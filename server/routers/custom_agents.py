import os
import uuid
import yaml
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, dependencies
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/custom_agents",
    tags=["Custom Agents"],
    responses={401: {"description": "Unauthorized"}}
)

AGENTS_DIR = "agents/custom"

def generate_agent_markdown(agent_data: schemas.CustomAgentCreate) -> str:
    metadata = {
        "identity": agent_data.identity.model_dump(),
        "system_rules": agent_data.system_rules.model_dump(),
        "capabilities": agent_data.capabilities,
        "constraints": agent_data.constraints
    }
    
    frontmatter = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
    
    content = f"""---
{frontmatter.strip()}
---

## System Prompt
{agent_data.system_prompt.strip()}
"""
    return content

@router.post("", response_model=schemas.CustomAgentOut, status_code=status.HTTP_201_CREATED)
def create_custom_agent(
    agent_data: schemas.CustomAgentCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    os.makedirs(AGENTS_DIR, exist_ok=True)
    
    # Generate a unique ID and filename
    agent_id = str(uuid.uuid4())
    filename = f"{agent_data.identity.name.lower().replace(' ', '-')}-{agent_id[:8]}.md"
    filepath = os.path.join(AGENTS_DIR, filename)
    
    # Write the markdown file
    try:
        content = generate_agent_markdown(agent_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create agent file: {str(e)}")
        
    # Save to database
    db_agent = models.CustomAgent(
        id=agent_id,
        name=agent_data.identity.name,
        role=agent_data.identity.role,
        filepath=filepath,
        tenant_id=tenant_id
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return db_agent

@router.get("", response_model=List[schemas.CustomAgentOut])
def list_custom_agents(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agents = db.query(models.CustomAgent).filter(models.CustomAgent.tenant_id == tenant_id).all()
    return agents

@router.get("/{agent_id}", response_model=schemas.CustomAgentOut)
def get_custom_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agent = db.query(models.CustomAgent).filter(
        models.CustomAgent.id == agent_id,
        models.CustomAgent.tenant_id == tenant_id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Custom Agent not found")
    return agent
