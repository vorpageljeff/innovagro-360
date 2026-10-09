"""Persist Instagram webhook conversations."""
from alembic import op
import sqlalchemy as sa

revision = '20261009_0007'
down_revision = '20261009_0006'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'crm_instagram_messages',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('organization_id', sa.Uuid(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('message_id', sa.String(200), nullable=False),
        sa.Column('lead_id', sa.Uuid(), sa.ForeignKey('crm_leads.id', ondelete='RESTRICT')),
        sa.Column('instagram_scoped_user_id', sa.String(64), nullable=False),
        sa.Column('username', sa.String(30)),
        sa.Column('direction', sa.String(10), nullable=False),
        sa.Column('text', sa.Text(), server_default='', nullable=False),
        sa.Column('attachment_type', sa.String(30)),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('organization_id', 'message_id', name='uq_crm_instagram_message'),
    )
    op.create_index('ix_crm_instagram_messages_organization_id', 'crm_instagram_messages', ['organization_id'])
    op.create_index('ix_crm_instagram_messages_lead_id', 'crm_instagram_messages', ['lead_id'])
    op.create_index('ix_crm_instagram_messages_instagram_scoped_user_id', 'crm_instagram_messages', ['instagram_scoped_user_id'])
    op.create_index('ix_crm_instagram_messages_username', 'crm_instagram_messages', ['username'])


def downgrade():
    raise RuntimeError('Preserve Instagram conversations before planning a rollback.')
