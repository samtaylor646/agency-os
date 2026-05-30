import pytest
import asyncio
from sqlalchemy import text
from server.database import SessionLocal, AsyncSessionLocal
from server.dependencies import get_async_db

@pytest.mark.asyncio
async def test_dual_engine_concurrency():
    """Test that both synchronous and asynchronous pools can be used concurrently without deadlocks."""
    
    # 1. Start a long-ish sync operation in a thread (or just simulate)
    def sync_db_op():
        db = SessionLocal()
        try:
            # Simple query to prove connection works
            result = db.execute(text("SELECT 1")).scalar()
            return result
        finally:
            db.close()

    # 2. Run async db op
    async def async_db_op():
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("SELECT 1"))
            return result.scalar()

    # Run them concurrently using asyncio.to_thread for the sync part
    sync_task = asyncio.to_thread(sync_db_op)
    async_task = asyncio.create_task(async_db_op())
    
    sync_result, async_result = await asyncio.gather(sync_task, async_task)
    
    assert sync_result == 1
    assert async_result == 1

@pytest.mark.asyncio
async def test_get_async_db_rollback_on_error():
    """Test that get_async_db correctly rolls back on exception."""
    db_gen = get_async_db()
    db = await db_gen.__anext__()
    
    try:
        # Simulate inserting or starting a transaction, then error
        await db.execute(text("CREATE TABLE IF NOT EXISTS test_rollback (id INTEGER PRIMARY KEY)"))
        await db.execute(text("INSERT INTO test_rollback (id) VALUES (1)"))
        
        # We simulate an exception occurring within the endpoint
        raise ValueError("Simulated error in endpoint")
    except ValueError:
        try:
            await db_gen.athrow(ValueError("Simulated error in endpoint"))
        except ValueError:
            pass # Expected
            
    # Now check if it was rolled back (id=1 should not exist)
    async with AsyncSessionLocal() as new_db:
        result = await new_db.execute(text("SELECT COUNT(*) FROM test_rollback WHERE id=1"))
        count = result.scalar()
        assert count == 0, "Transaction was not rolled back!"

    # Clean up
    async with AsyncSessionLocal() as cleanup_db:
        await cleanup_db.execute(text("DROP TABLE IF EXISTS test_rollback"))
        await cleanup_db.commit()

