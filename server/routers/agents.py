import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import yaml

from .. import models, schemas, dependencies
from ..dependencies import get_async_db

router = APIRouter(
    prefix="/api/v1/agents",
    tags=["Agents"],
    responses={401: {"description": "Unauthorized"}}
)

AGENTS_DIR = "agents/custom"

def generate_agent_markdown(agent_data: schemas.CustomAgentCreate) -> str:
    # If the payload comes in flattened format (like from the UI), map it to the structure
    name = agent_data.name or agent_data.identity.name
    role = agent_data.role or agent_data.identity.role
    description = agent_data.description or agent_data.identity.description
    color = agent_data.color or agent_data.identity.color
    emoji = agent_data.emoji or agent_data.identity.emoji
    vibe = agent_data.vibe or agent_data.identity.vibe
    intro_paragraph = getattr(agent_data, "intro_paragraph", "") or getattr(agent_data.identity, "intro_paragraph", "")
    
    personality = agent_data.personality or agent_data.system_rules.personality
    experience = agent_data.experience or agent_data.system_rules.experience
    memory = agent_data.memory or agent_data.system_rules.memory
    
    mission = agent_data.mission or agent_data.system_rules.mission
    rules = agent_data.rules or agent_data.system_rules.rules
    deliverables = agent_data.deliverables or agent_data.system_rules.deliverables
    communication = agent_data.communication or agent_data.system_rules.communication
    learning = agent_data.learning or agent_data.system_rules.learning
    success_metrics = agent_data.success_metrics or agent_data.system_rules.success_metrics
    advanced_capabilities = agent_data.advanced_capabilities or agent_data.system_rules.advanced_capabilities
    instructions_reference = getattr(agent_data, "instructions_reference", "") or getattr(agent_data.system_rules, "instructions_reference", "")

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

{f"---" if instructions_reference else ""}

{f"**Instructions Reference**: {instructions_reference}" if instructions_reference else ""}
"""
    return content

@router.post("", response_model=schemas.CustomAgentOut, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: schemas.CustomAgentCreate,
    db: AsyncSession = Depends(get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    os.makedirs(AGENTS_DIR, exist_ok=True)
    
    name = agent_data.name or agent_data.identity.name
    role = agent_data.role or agent_data.identity.role
    
    # Generate a unique ID and filename
    agent_id = str(uuid.uuid4())
    filename = f"{name.lower().replace(' ', '-')}-{agent_id[:8]}.md"
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
        name=name,
        role=role,
        filepath=filepath,
        tenant_id=tenant_id
    )
    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    
    return db_agent

@router.get("", response_model=List[schemas.CustomAgentOut])
async def list_agents(
    db: AsyncSession = Depends(get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    result = await db.execute(select(models.CustomAgent).filter(models.CustomAgent.tenant_id == tenant_id))
    return result.scalars().all()
