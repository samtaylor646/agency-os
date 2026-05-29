"""Update Template model for Phase 6

Revision ID: 63dd300a8382
Revises: 202605260000
Create Date: 2026-05-29 16:13:21.643055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63dd300a8382'
down_revision: Union[str, Sequence[str], None] = '202605260000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('templates') as batch_op:
        batch_op.add_column(sa.Column('workspace_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('dag_configuration', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('agent_definitions', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('required_api_capabilities', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('complexity_rating', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('is_system', sa.Boolean(), nullable=True))

    op.execute("UPDATE templates SET dag_configuration = '{}', agent_definitions = '{}'")
    
    with op.batch_alter_table('templates') as batch_op:
        batch_op.alter_column('dag_configuration', nullable=False)
        batch_op.alter_column('agent_definitions', nullable=False)

        batch_op.create_foreign_key('fk_templates_workspace_id', 'workspaces', ['workspace_id'], ['id'])

        batch_op.drop_column('template_type')
        batch_op.drop_column('content')
        batch_op.drop_column('version')
        batch_op.drop_column('tenant_id')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('templates') as batch_op:
        batch_op.add_column(sa.Column('tenant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('version', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('content', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('template_type', sa.String(length=255), nullable=True))
        
        batch_op.drop_constraint('fk_templates_workspace_id', type_='foreignkey')

        batch_op.drop_column('is_system')
        batch_op.drop_column('complexity_rating')
        batch_op.drop_column('required_api_capabilities')
        batch_op.drop_column('agent_definitions')
        batch_op.drop_column('dag_configuration')
        batch_op.drop_column('workspace_id')
