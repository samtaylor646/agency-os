with open("server/routers/custom_agents.py", "r") as f:
    code = f.read()

import re

old_block = """        db_agent = models.CustomAgent(
            id=agent_id,
            name=name,
            role=role,
            tenant_id=tenant_id
        )
        db.add(db_agent)
        db.flush()
        
        # Write to storage
        filepath = config_service.save_agent_config(tenant_id, agent_id, agent_data)
        
        db_agent.filepath = filepath
        db.commit()"""

new_block = """        # Write to storage
        filepath = config_service.save_agent_config(tenant_id, agent_id, agent_data)
        
        db_agent = models.CustomAgent(
            id=agent_id,
            name=name,
            role=role,
            tenant_id=tenant_id,
            filepath=filepath
        )
        db.add(db_agent)
        db.commit()"""

code = code.replace(old_block, new_block)

with open("server/routers/custom_agents.py", "w") as f:
    f.write(code)
