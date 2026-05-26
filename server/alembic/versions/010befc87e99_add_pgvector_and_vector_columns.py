"""add pgvector and vector columns

Revision ID: 010befc87e99
Revises: 2314551a72e6
Create Date: 2026-05-26 15:37:03.308877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '010befc87e99'
down_revision: Union[str, Sequence[str], None] = '2314551a72e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column('documents', sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('documents', 'embedding')
