import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas, dependencies
from ..database import get_db
from ..services.agent_config_service import get_storage_backend, AgentConfigService

router = APIRouter(
    prefix="/api/v1/custom_agents",
    tags=["Agents"],
    responses={401: {"description": "Unauthorized"}}
)

@router.post("", response_model=schemas.CustomAgentOut, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: schemas.CustomAgentCreate,
    db: AsyncSession = Depends(dependencies.get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    filepath = None
    config_service = AgentConfigService(get_storage_backend())
    try:
        name = agent_data.identity.name
        role = agent_data.identity.role
        
        agent_id = str(uuid.uuid4())
        
        # Write to storage
        filepath = config_service.save_agent_config(tenant_id, agent_id, agent_data)
        
        db_agent = models.CustomAgent(
            id=agent_id,
            name=name,
            role=role,
            tenant_id=tenant_id,
            filepath=filepath
        )
        db.add(db_agent)
        await db.commit()
        await db.refresh(db_agent)
        
        return db_agent
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")

@router.get("", response_model=List[schemas.CustomAgentOut])
async def list_agents(
    db: AsyncSession = Depends(dependencies.get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    agents = (await db.execute(select(models.CustomAgent).filter(models.CustomAgent.tenant_id == tenant_id))).scalars().all()
    return agents

# B2-1: Implement PUT /api/custom-agents/{agent_id} endpoint
@router.put("/{agent_id}", response_model=schemas.CustomAgentOut)
async def update_agent(
    agent_id: str,
    agent_data: schemas.CustomAgentCreate,
    db: AsyncSession = Depends(dependencies.get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    db_agent = (await db.execute(select(models.CustomAgent).filter(
        models.CustomAgent.id == agent_id,
        models.CustomAgent.tenant_id == tenant_id
    ))).scalars().first()
    
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    config_service = AgentConfigService(get_storage_backend())
    old_filepath = db_agent.filepath
    new_filepath = None
    try:
        db_agent.name = agent_data.identity.name
        db_agent.role = agent_data.identity.role
        await db.flush()
        
        # Generate new markdown and overwrite file (or create new if path changes)
        # Using the same agent_id will overwrite the file in storage layer
        new_filepath = config_service.save_agent_config(tenant_id, agent_id, agent_data)
        
        db_agent.filepath = new_filepath
        
        await db.commit()
        await db.refresh(db_agent)
        return db_agent
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update agent: {str(e)}")

# B2-2: Implement DELETE /api/custom-agents/{agent_id} endpoint
@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: AsyncSession = Depends(dependencies.get_async_db),
    tenant_id: int = Depends(dependencies.get_api_or_user_tenant_context)
):
    db_agent = (await db.execute(select(models.CustomAgent).filter(
        models.CustomAgent.id == agent_id,
        models.CustomAgent.tenant_id == tenant_id
    ))).scalars().first()
    
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    config_service = AgentConfigService(get_storage_backend())
    filepath = db_agent.filepath
    
    try:
        # B3-1: Transactional integrity: delete from DB first, if succeeds delete from storage
        await db.delete(db_agent)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete agent from database: {str(e)}")
        
    try:
        config_service.delete_agent_config(filepath)
    except Exception as e:
        print(f"Warning: Failed to delete agent file {filepath}: {e}")
        # Not raising 500 here since DB deletion was successful, avoiding zombie DB records
    
    return None
