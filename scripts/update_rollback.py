import sys

def update_state_manager():
    with open('server/core/state_manager.py', 'r') as f:
        content = f.read()

    new_method = """
    def rollback_nodes(self, workflow_id: str, tenant_id: str, workflow_name: str, nodes_to_reset: list) -> bool:
        if not SessionLocal or not WorkflowExecution:
            return False
            
        db = SessionLocal()
        try:
            exec_record = db.query(WorkflowExecution).filter(WorkflowExecution.id == workflow_id).first()
            if not exec_record:
                return False
                
            state = exec_record.execution_context or {}
            completed_nodes = exec_record.completed_nodes or []
            failed_nodes = exec_record.failed_nodes or []
            
            for node_id in nodes_to_reset:
                if node_id in state:
                    state[node_id]["status"] = "pending"
                    if "result" in state[node_id]:
                        del state[node_id]["result"]
                    if "error" in state[node_id]:
                        del state[node_id]["error"]
                if node_id in completed_nodes:
                    completed_nodes.remove(node_id)
                if node_id in failed_nodes:
                    failed_nodes.remove(node_id)

            exec_record.execution_context = state
            exec_record.completed_nodes = completed_nodes
            exec_record.failed_nodes = failed_nodes
            exec_record.status = "PAUSED"
            db.commit()
            return True
        except Exception as e:
            print(f"Failed to rollback state: {e}")
            return False
        finally:
            db.close()
"""
    # Insert new_method at the end of StateManager class
    # The last method is inject_intervention
    content += new_method

    with open('server/core/state_manager.py', 'w') as f:
        f.write(content)

def update_orchestrator():
    with open('server/services/orchestrator_service.py', 'r') as f:
        content = f.read()

    new_methods = """
    def get_downstream_nodes(self, target_node_id: str) -> list:
        downstream = set()
        queue = [target_node_id]
        while queue:
            current = queue.pop(0)
            for child in self.edges.get(current, []):
                if child not in downstream:
                    downstream.add(child)
                    queue.append(child)
        return list(downstream)

    async def handle_rollback_request(self, tenant_id: str, node_id: str):
        # Pause pipeline handled implicitly by saving state as PAUSED
        downstream_nodes = self.get_downstream_nodes(node_id)
        nodes_to_reset = downstream_nodes + [node_id]
        
        self.load_state()
        
        for n in nodes_to_reset:
            if n in self.state:
                self.state[n]["status"] = "pending"
                if "result" in self.state[n]:
                    del self.state[n]["result"]
                if "error" in self.state[n]:
                    del self.state[n]["error"]

        if self.state_manager:
            self.state_manager.rollback_nodes(self.workflow_id, tenant_id, self.workflow_name, nodes_to_reset)
            
        if message_broker:
            await message_broker.publish(str(tenant_id), {
                "type": "ROLLBACK_COMPLETED",
                "workflow_id": self.workflow_id,
                "node_id": node_id,
                "state": self.state
            })
"""
    content += new_methods

    with open('server/services/orchestrator_service.py', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    update_state_manager()
    update_orchestrator()
    print("Done")
