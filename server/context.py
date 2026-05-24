import contextvars

# Context variable to hold the tenant ID for the current request/execution
tenant_id_context = contextvars.ContextVar("tenant_id", default=None)

def get_tenant_id() -> str:
    """Retrieve the current tenant ID from context."""
    return tenant_id_context.get()

def set_tenant_id(tenant_id: str):
    """Set the current tenant ID in context."""
    tenant_id_context.set(tenant_id)
