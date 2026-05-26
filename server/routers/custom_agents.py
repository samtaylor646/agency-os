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
    # If the payload comes in flattened format (like from the UI), map it to the structure
    name = agent_data.name or agent_data.identity.name
    role = agent_data.role or agent_data.identity.role
    description = agent_data.description or agent_data.identity.description
    color = agent_data.color or agent_data.identity.color
    emoji = agent_data.emoji or agent_data.identity.emoji
    vibe = agent_data.vibe or agent_data.identity.vibe
    intro_paragraph = getattr(agent_data, "intro_paragraph", "") or getattr(agent_data.identity, "intro_paragraph", "")
    
    personality = getattr(agent_data, "personality", "") or getattr(agent_data.system_rules, "personality", "")
    experience = getattr(agent_data, "experience", "") or getattr(agent_data.system_rules, "experience", "")
    memory = getattr(agent_data, "memory", "") or getattr(agent_data.system_rules, "memory", "")
    
    mission = getattr(agent_data, "mission", "") or getattr(agent_data.system_rules, "mission", "")
    rules = getattr(agent_data, "rules", "") or getattr(agent_data.system_rules, "rules", "")
    deliverables = getattr(agent_data, "deliverables", "") or getattr(agent_data.system_rules, "deliverables", "")
    communication = getattr(agent_data, "communication", "") or getattr(agent_data.system_rules, "communication", "")
    learning = getattr(agent_data, "learning", "") or getattr(agent_data.system_rules, "learning", "")
    success_metrics = getattr(agent_data, "success_metrics", "") or getattr(agent_data.system_rules, "success_metrics", "")
    
    # Handle capabilities list if provided, otherwise fallback to advanced_capabilities string
    if getattr(agent_data, "capabilities", None):
        advanced_capabilities = "\n".join([f"- {cap}" for cap in agent_data.capabilities])
    else:
        advanced_capabilities = getattr(agent_data, "advanced_capabilities", "") or getattr(agent_data.system_rules, "advanced_capabilities", "")
        
    if getattr(agent_data, "constraints", None):
        rules = "\n".join([f"- {c}" for c in agent_data.constraints])
    else:
        rules = getattr(agent_data, "rules", "") or getattr(agent_data.system_rules, "rules", "")
        
    system_prompt = agent_data.system_prompt or ""
        
    instructions_reference = getattr(agent_data, "instructions_reference", "") or getattr(agent_data.system_rules, "instructions_reference", "")

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
    try:
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
            import traceback
            traceback.print_exc()
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
        db.commit()
        db.refresh(db_agent)
        
        return db_agent
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("", response_model=List[schemas.CustomAgentOut])
def list_agents(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agents = db.query(models.CustomAgent).filter(models.CustomAgent.tenant_id == tenant_id).all()
    return agents
