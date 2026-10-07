"""Inbound WhatsApp contacts and human handoff."""
from alembic import op
import sqlalchemy as sa

revision = '20261007_0004'
down_revision = '20261007_0003'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('crm_leads', 'instagram', existing_type=sa.String(30), nullable=True)
    op.add_column('crm_leads', sa.Column('bot_paused', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('crm_automation_rules', sa.Column('position', sa.Integer(), nullable=False, server_default='100'))
    op.add_column('crm_automation_rules', sa.Column('handoff', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    raise RuntimeError('WhatsApp contacts may lack Instagram. Plan recovery before reverting.')
