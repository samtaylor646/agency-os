import os
import uuid
import boto3
from botocore.exceptions import ClientError
from typing import Optional
from .. import schemas

class StorageBackend:
    def write_file(self, tenant_id: int, agent_id: str, content: str) -> str:
        raise NotImplementedError

    def delete_file(self, filepath: str):
        raise NotImplementedError

class LocalStorageBackend(StorageBackend):
    def __init__(self, base_dir="agents/custom"):
        self.base_dir = base_dir

    def write_file(self, tenant_id: int, agent_id: str, content: str) -> str:
        tenant_dir = os.path.join(self.base_dir, f"tenants/{tenant_id}/custom_agents")
        os.makedirs(tenant_dir, exist_ok=True)
        filepath = os.path.join(tenant_dir, f"{agent_id}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def delete_file(self, filepath: str):
        if os.path.exists(filepath):
            os.remove(filepath)

class S3StorageBackend(StorageBackend):
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def write_file(self, tenant_id: int, agent_id: str, content: str) -> str:
        # S3 path follows tenant isolation
        s3_key = f"tenants/{tenant_id}/custom_agents/{agent_id}.md"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=content.encode('utf-8')
            )
            return f"s3://{self.bucket_name}/{s3_key}"
        except ClientError as e:
            raise Exception(f"Failed to write to S3: {e}")

    def delete_file(self, filepath: str):
        if filepath.startswith(f"s3://{self.bucket_name}/"):
            s3_key = filepath.replace(f"s3://{self.bucket_name}/", "")
            try:
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=s3_key
                )
            except ClientError as e:
                raise Exception(f"Failed to delete from S3: {e}")

def get_storage_backend() -> StorageBackend:
    storage_type = os.getenv("STORAGE_BACKEND", "local").lower()
    if storage_type == "s3":
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required when STORAGE_BACKEND=s3")
        return S3StorageBackend(bucket_name)
    else:
        return LocalStorageBackend()

def generate_agent_markdown(agent_data: schemas.CustomAgentCreate) -> str:
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
        rules_list = "\n".join([f"- {c}" for c in agent_data.constraints])
        rules = f"{rules}\n{rules_list}"
        
    system_prompt = getattr(agent_data, 'system_prompt', "")
        
    instructions_reference = getattr(agent_data.system_rules, 'instructions_reference', "")

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
{"---" if instructions_reference else ""}

{f"**Instructions Reference**: {instructions_reference}" if instructions_reference else ""}
"""
    return content

class AgentConfigService:
    def __init__(self, storage_backend: StorageBackend):
        self.storage_backend = storage_backend

    def save_agent_config(self, tenant_id: int, agent_id: str, agent_data: schemas.CustomAgentCreate) -> str:
        content = generate_agent_markdown(agent_data)
        return self.storage_backend.write_file(tenant_id, agent_id, content)

    def delete_agent_config(self, filepath: str):
        self.storage_backend.delete_file(filepath)
