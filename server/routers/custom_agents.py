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
        "name": agent_data.name,
        "role": agent_data.role,
        "description": agent_data.description
    }
    
    frontmatter = yaml.dump(metadata, default_flow_style=False)
    
    content = f"""---
{frontmatter.strip()}
---

## System Prompt
{agent_data.system_prompt.strip()}

## Capabilities
{agent_data.capabilities.strip()}

## Guardrails
{agent_data.guardrails.strip()}
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
    filename = f"{agent_data.name.lower().replace(' ', '-')}-{agent_id[:8]}.md"
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
        name=agent_data.name,
        role=agent_data.role,
        filepath=filepath
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
    # Depending on requirements, we could scope by tenant_id if CustomAgent had tenant_id.
    # Currently models.CustomAgent doesn't have tenant_id, so it returns all globally custom agents.
    agents = db.query(models.CustomAgent).all()
    return agents

@router.get("/{agent_id}", response_model=schemas.CustomAgentOut)
def get_custom_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agent = db.query(models.CustomAgent).filter(models.CustomAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Custom Agent not found")
    return agent
