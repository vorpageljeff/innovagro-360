"""Persistent WhatsApp drafts and manual-send claims."""
from alembic import op
import sqlalchemy as sa
revision = '20261009_0005'
down_revision = '20261007_0004'
branch_labels = None
depends_on = None

def columns():
    return [sa.Column('id', sa.Uuid(), primary_key=True), sa.Column('organization_id', sa.Uuid(), sa.ForeignKey('organizations.id'), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)]

def upgrade():
    op.create_table('crm_whatsapp_drafts', *columns(), sa.Column('lead_id', sa.Uuid(), sa.ForeignKey('crm_leads.id', ondelete='RESTRICT')), sa.Column('text', sa.Text(), nullable=False), sa.Column('request_id', sa.Uuid(), nullable=False), sa.UniqueConstraint('organization_id', 'lead_id', name='uq_whatsapp_draft_lead'))
    op.create_table('crm_whatsapp_outbound', *columns(), sa.Column('lead_id', sa.Uuid(), sa.ForeignKey('crm_leads.id', ondelete='RESTRICT'), nullable=False), sa.Column('request_id', sa.Uuid(), nullable=False), sa.Column('phone', sa.String(16), nullable=False), sa.Column('text', sa.Text(), nullable=False), sa.Column('state', sa.String(20), nullable=False), sa.UniqueConstraint('organization_id', 'request_id', name='uq_whatsapp_outbound_request'))
    op.create_index('ix_crm_whatsapp_outbound_lead_id', 'crm_whatsapp_outbound', ['lead_id'])

def downgrade():
    raise RuntimeError('Preserve manual-send history before planning a rollback.')
