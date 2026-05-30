import re

with open('scripts/central_runner.py', 'r') as f:
    content = f.read()

execute_workflow_code = """    async def execute_workflow(self, tenant_id: str):
        try:
            levels = self.get_topological_sort()
        except ValueError as e:
            return {"status": "FAILED", "error": str(e)}

        self.load_state()
        self._save_state(tenant_id, "RUNNING")
        
        if message_broker and not self.state:
            await message_broker.publish(str(tenant_id), {
                "type": "workflow_start",
                "workflow_id": self.workflow_id,
                "workflow_name": self.workflow_name,
                "nodes": {k: {"agent_name": v["agent_name"], "task": v["task"]} for k, v in self.nodes.items()},
                "edges": dict(self.edges)
            })
            
        results = self.state.copy()
        has_failure = False
        
        try:
            from server.services.kill_switch import kill_switch
        except ImportError:
            kill_switch = None

        for level in levels:
            if kill_switch and kill_switch.is_active(tenant_id):
                final_status = "KILLED_BY_SWITCH"
                self._save_state(tenant_id, final_status)
                if message_broker:
                    await message_broker.publish(str(tenant_id), {
                        "type": "workflow_failed",
                        "workflow_id": self.workflow_id,
                        "error": "Workflow execution halted by LLM Kill Switch."
                    })
                return {"status": final_status, "results": results, "error": "Workflow execution halted by LLM Kill Switch."}

            tasks = []
            node_ids_in_tasks = []
            has_pause = False
            
            for node_id in level:
                node_status = self.state.get(node_id, {}).get("status")
                
                # If node is already successfully completed
                if node_status in ["success", "COMPLETED"]:
                    continue
                
                # If node is currently paused and awaiting intervention
                if node_status in ["PAUSED_AWAITING_APPROVAL", "PAUSED_ERROR_ESCALATION"]:
                    has_pause = True
                    continue
                
                # Check dependencies state
                skip_node = False
                for parent in self.incoming_edges.get(node_id, []):
                    parent_status = results.get(parent, {}).get("status")
                    if parent_status in ["failed", "skipped", "PAUSED_ERROR_ESCALATION", "PAUSED_AWAITING_APPROVAL"]:
                        skip_node = True
                        break
                        
                if skip_node:
                    results[node_id] = {"status": "skipped", "error": "Parent node failed, skipped, or paused"}
                    self.state[node_id] = results[node_id]
                    continue
                    
                node_info = self.nodes[node_id]
                
                context_data = {}
                for parent_node in self.incoming_edges.get(node_id, []):
                    parent_res = results.get(parent_node, {})
                    if "result" in parent_res:
                        context_data[parent_node] = parent_res["result"]
                
                if node_status == "INTERVENED":
                    intervened_context = self.state.get(node_id, {}).get("context_data", {})
                    if "HUMAN_INTERVENTION" in intervened_context:
                        context_data["HUMAN_INTERVENTION"] = intervened_context["HUMAN_INTERVENTION"]
                
                required_inputs = node_info.get("required_inputs", [])
                if required_inputs:
                    filtered_context = {}
                    for req in required_inputs:
                        for parent_res in context_data.values():
                            if isinstance(parent_res, dict) and req in parent_res:
                                filtered_context[req] = parent_res[req]
                    
                    missing_inputs = [req for req in required_inputs if req not in filtered_context]
                    if missing_inputs:
                        results[node_id] = {"status": "failed", "error": f"Schema validation failed. Missing required inputs: {missing_inputs}"}
                        self.state[node_id] = results[node_id]
                        has_failure = True
                        continue
                        
                    context_data = filtered_context

                tasks.append(
                    execute_node_with_retry(
                        node_id=node_id,
                        agent_name=node_info["agent_name"],
                        task=node_info["task"],
                        context_data=context_data,
                        tenant_id=tenant_id
                    )
                )
                node_ids_in_tasks.append(node_id)
            
            if tasks:
                level_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for node_id, result in zip(node_ids_in_tasks, level_results):
                    if isinstance(result, Exception):
                        # PAUSED_ERROR_ESCALATION
                        res_dict = {
                            "status": "PAUSED_ERROR_ESCALATION", 
                            "error": str(result),
                            "node_id": node_id
                        }
                        results[node_id] = res_dict
                        has_pause = True
                        
                        if message_broker:
                            asyncio.create_task(message_broker.publish(str(tenant_id), {
                                "type": "pipeline_paused",
                                "node_id": node_id,
                                "reason": "error_escalation",
                                "error": str(result)
                            }))
                            asyncio.create_task(message_broker.publish(str(tenant_id), {
                                "type": "error_escalation",
                                "node_id": node_id,
                                "error": str(result)
                            }))
                            
                    elif hasattr(result, 'dict'):
                        res_dict = result.dict()
                        if res_dict["status"] == "success" and self.nodes[node_id].get("requires_human_approval"):
                            res_dict["status"] = "PAUSED_AWAITING_APPROVAL"
                            has_pause = True
                            if message_broker:
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "pipeline_paused",
                                    "node_id": node_id,
                                    "reason": "awaiting_approval"
                                }))
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "awaiting_approval",
                                    "node_id": node_id,
                                    "result": res_dict.get("result")
                                }))
                        elif res_dict["status"] == "failed":
                            res_dict["status"] = "PAUSED_ERROR_ESCALATION"
                            has_pause = True
                            if message_broker:
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "pipeline_paused",
                                    "node_id": node_id,
                                    "reason": "error_escalation",
                                    "error": res_dict.get("error")
                                }))
                                asyncio.create_task(message_broker.publish(str(tenant_id), {
                                    "type": "error_escalation",
                                    "node_id": node_id,
                                    "error": res_dict.get("error")
                                }))
                        else:
                            if res_dict["status"] == "failed":
                                has_failure = True
                        
                        results[node_id] = res_dict
                        
                    self.state[node_id] = results[node_id]
                    
            if has_pause:
                self._save_state(tenant_id, "PAUSED")
                return {"status": "PAUSED", "results": results}
                
            self._save_state(tenant_id, "RUNNING")
                
        final_status = "PARTIAL_FAILURE" if has_failure else "COMPLETED"
        self._save_state(tenant_id, final_status)
        
        if message_broker:
            await message_broker.publish(str(tenant_id), {
                "type": "workflow_complete",
                "workflow_id": self.workflow_id,
                "status": final_status,
                "results": results
            })
            
        return {"status": final_status, "results": results}"""

start_idx = content.find("    async def execute_workflow(self, tenant_id: str):")
if start_idx != -1:
    new_content = content[:start_idx] + execute_workflow_code + "\n"
    with open('scripts/central_runner.py', 'w') as f:
        f.write(new_content)
    print("Updated successfully")
else:
    print("Could not find execute_workflow")

