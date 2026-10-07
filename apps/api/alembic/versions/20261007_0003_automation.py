"""Priorities, WhatsApp identity and persisted automation rules."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '20261007_0003'
down_revision = '20260921_0002'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('crm_leads', sa.Column('priority', sa.String(10), nullable=False, server_default='media'))
    op.add_column('crm_leads', sa.Column('phone', sa.String(16), nullable=True))
    op.create_index('uq_crm_lead_phone', 'crm_leads', ['organization_id', 'phone'], unique=True)
    common = lambda: [sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('organization_id', UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())]
    op.create_table('crm_automation_rules', *common(),
        sa.Column('name', sa.String(120), nullable=False), sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('contains', sa.String(200), nullable=False), sa.Column('reply', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(10)), sa.Column('status', sa.String(30)))
    op.create_table('crm_automation_receipts', *common(),
        sa.Column('message_id', sa.String(200), nullable=False),
        sa.Column('lead_id', UUID(as_uuid=True), sa.ForeignKey('crm_leads.id', ondelete='RESTRICT')),
        sa.Column('incoming', sa.Text(), nullable=False), sa.Column('reply', sa.Text(), nullable=False),
        sa.Column('state', sa.String(30), nullable=False),
        sa.UniqueConstraint('organization_id', 'message_id', name='uq_crm_webhook_message'))
    for table in ('crm_automation_rules', 'crm_automation_receipts'):
        op.create_index(f'ix_{table}_organization_id', table, ['organization_id'])


def downgrade():
    raise RuntimeError('Preserve message history; plan recovery before removing automation tables.')
