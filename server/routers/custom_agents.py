import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import yaml

from .. import models, schemas, dependencies
from ..database import get_db

router = APIRouter(
    prefix="/api/v1/custom_agents",
    tags=["Agents"],
    responses={401: {"description": "Unauthorized"}}
)

AGENTS_DIR = "agents/custom"

def generate_agent_markdown(agent_data: schemas.CustomAgentCreate) -> str:
    # Map from the strict nested structure
    name = agent_data.identity.name
    role = agent_data.identity.role
    description = agent_data.identity.description
    color = agent_data.identity.color
    emoji = agent_data.identity.emoji
    vibe = agent_data.identity.vibe
    intro_paragraph = agent_data.identity.intro_paragraph
    
    personality = agent_data.system_rules.personality
    experience = agent_data.system_rules.experience
    memory = agent_data.system_rules.memory
    
    mission = agent_data.system_rules.mission
    rules = agent_data.system_rules.rules
    deliverables = agent_data.system_rules.deliverables
    communication = agent_data.system_rules.communication
    learning = agent_data.system_rules.learning
    success_metrics = agent_data.system_rules.success_metrics
    
    if agent_data.capabilities:
        advanced_capabilities = "\n".join([f"- {cap}" for cap in agent_data.capabilities])
    else:
        advanced_capabilities = agent_data.system_rules.advanced_capabilities
        
    if agent_data.constraints:
        rules = "\n".join([f"- {c}" for c in agent_data.constraints])
        
    system_prompt = agent_data.system_prompt or ""
        
    instructions_reference = agent_data.system_rules.instructions_reference

    if system_prompt:
        system_prompt_section = f"## 🤖 System Prompt\n{system_prompt}\n"
    else:
        system_prompt_section = ""

    content = f"""---
name: {name}
description: {description}
color: {color}
emoji: {emoji}
vibe: {vibe}
---

# {name} Agent Personality

{intro_paragraph}

## 🧠 Your Identity & Memory
- **Role**: {role}
- **Personality**: {personality}
- **Memory**: {memory}
- **Experience**: {experience}

## 🎯 Your Core Mission
{mission}

## 🚨 Critical Rules You Must Follow
{rules}

## 📋 Your Architecture Deliverables
{deliverables}

## 💭 Your Communication Style
{communication}

## 🔄 Learning & Memory
{learning}

## 🎯 Your Success Metrics
{success_metrics}

## 🚀 Advanced Capabilities
{advanced_capabilities}

{system_prompt_section}
{f"---" if instructions_reference else ""}

{f"**Instructions Reference**: {instructions_reference}" if instructions_reference else ""}
"""
    return content

@router.post("", response_model=schemas.CustomAgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_data: schemas.CustomAgentCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    filepath = None
    try:
        os.makedirs(AGENTS_DIR, exist_ok=True)
        
        name = agent_data.identity.name
        role = agent_data.identity.role
        
        # Generate a unique ID and filename
        agent_id = str(uuid.uuid4())
        filename = f"{name.lower().replace(' ', '-')}-{agent_id[:8]}.md"
        filepath = os.path.join(AGENTS_DIR, filename)
        
        # 1. DB Flush first to ensure we can insert (transaction safety)
        db_agent = models.CustomAgent(
            id=agent_id,
            name=name,
            role=role,
            filepath=filepath,
            tenant_id=tenant_id
        )
        db.add(db_agent)
        db.flush() # Will raise if DB error occurs
        
        # 2. Write the markdown file
        content = generate_agent_markdown(agent_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        # 3. DB Commit
        db.commit()
        db.refresh(db_agent)
        
        return db_agent
    except Exception as e:
        db.rollback()
        # Clean up file if DB commit failed after file was written
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")

@router.get("", response_model=List[schemas.CustomAgentOut])
def list_agents(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agents = db.query(models.CustomAgent).filter(models.CustomAgent.tenant_id == tenant_id).all()
    return agents
