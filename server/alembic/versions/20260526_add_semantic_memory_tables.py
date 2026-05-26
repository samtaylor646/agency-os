"""add semantic memory tables and HNSW indexes

Revision ID: 202605260000
Revises: 010befc87e99
Create Date: 2026-05-26 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '202605260000'
down_revision: Union[str, Sequence[str], None] = '010befc87e99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure vector extension is present
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # We already have a `documents` table from the previous migration, 
    # but we might need to modify it or create new ones as per spec.
    # The spec mentions document_chunks, agent_sessions, session_messages
    
    op.create_table(
        'document_chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('workspace_id', sa.Integer(), index=True, nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('text_content', sa.Text(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True)
    )
    
    # HNSW Index for document_chunks
    op.execute(
        "CREATE INDEX document_chunks_embedding_idx ON document_chunks "
        "USING hnsw (embedding vector_cosine_ops);"
    )

    op.create_table(
        'agent_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('workspace_id', sa.Integer(), index=True, nullable=False),
        sa.Column('agent_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    op.create_table(
        'session_messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agent_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # HNSW Index for session_messages
    op.execute(
        "CREATE INDEX session_messages_embedding_idx ON session_messages "
        "USING hnsw (embedding vector_cosine_ops);"
    )

    # Note: We assume the existing 'documents' table has what it needs, 
    # but the spec asks for Alembic migration for documents too. 
    # The previous migration (010befc87e99) added embedding to documents.
    # We should add an HNSW index to documents if it doesn't have one.
    op.execute(
        "CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents "
        "USING hnsw (embedding vector_cosine_ops);"
    )


def downgrade() -> None:
    op.drop_index('session_messages_embedding_idx', table_name='session_messages', postgresql_using='hnsw')
    op.drop_table('session_messages')
    
    op.drop_table('agent_sessions')
    
    op.drop_index('document_chunks_embedding_idx', table_name='document_chunks', postgresql_using='hnsw')
    op.drop_table('document_chunks')
    
    op.execute("DROP INDEX IF EXISTS documents_embedding_idx;")

