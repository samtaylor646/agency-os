from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Any
from ..models import DocumentChunk
from ..embeddings import get_embedding_provider

async def search_documents(db: Session, workspace_id: int, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform vector similarity search for document chunks.
    """
    provider = get_embedding_provider()
    query_embedding = await provider.get_embedding(query)
    
    # Using pgvector <=> operator for cosine distance
    # Lower distance = higher similarity
    stmt = (
        select(
            DocumentChunk.text_content, 
            DocumentChunk.document_id,
            DocumentChunk.embedding.cosine_distance(query_embedding).label("distance")
        )
        .where(DocumentChunk.workspace_id == workspace_id)
        .order_by("distance")
        .limit(top_k)
    )
    
    results = db.execute(stmt).all()
    
    return [
        {
            "text_content": row.text_content,
            "document_id": row.document_id,
            "distance": row.distance,
            "similarity": 1.0 - (row.distance if row.distance is not None else 1.0)
        }
        for row in results
    ]
