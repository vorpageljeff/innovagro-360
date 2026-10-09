"""Per-user read acknowledgments for the WhatsApp inbox."""
from alembic import op
import sqlalchemy as sa
revision = '20261009_0006'
down_revision = '20261009_0005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('crm_whatsapp_reads',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('organization_id', sa.Uuid(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('lead_id', sa.Uuid(), sa.ForeignKey('crm_leads.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('receipt_id', sa.Uuid(), sa.ForeignKey('crm_automation_receipts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('organization_id', 'user_id', 'receipt_id', name='uq_whatsapp_read_user_receipt'))
    op.create_index('ix_crm_whatsapp_reads_organization_id', 'crm_whatsapp_reads', ['organization_id'])
    op.create_index('ix_crm_whatsapp_reads_lead_id', 'crm_whatsapp_reads', ['lead_id'])

def downgrade():
    raise RuntimeError('Preserve read acknowledgments before planning a rollback.')
