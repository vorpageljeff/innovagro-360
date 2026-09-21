"""Add CRM tables; preserve existing identity and business data."""
from alembic import op

revision = '20260921_0002'
down_revision = '20260910_0001'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE TABLE IF NOT EXISTS crm_leads (\n\tname VARCHAR(160) NOT NULL, \n\tinstagram VARCHAR(30) NOT NULL, \n\tcity VARCHAR(160) NOT NULL, \n\tstatus VARCHAR(30) NOT NULL, \n\tlast_contact_on DATE, \n\tnext_contact_on DATE, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tupdated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\torganization_id UUID NOT NULL, \n\tCONSTRAINT pk_crm_leads PRIMARY KEY (id), \n\tCONSTRAINT uq_crm_lead_profile UNIQUE (organization_id, instagram), \n\tCONSTRAINT fk_crm_leads_organization_id_organizations FOREIGN KEY(organization_id) REFERENCES organizations (id) ON DELETE RESTRICT\n)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_crm_leads_organization_id ON crm_leads (organization_id)')
    op.execute('CREATE TABLE IF NOT EXISTS crm_lead_activities (\n\tlead_id UUID NOT NULL, \n\tevent_key VARCHAR(120) NOT NULL, \n\tkind VARCHAR(20) NOT NULL, \n\trequested_status VARCHAR(30), \n\trequested_next_contact_on DATE, \n\toccurred_on DATE NOT NULL, \n\tnote TEXT NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tid UUID NOT NULL, \n\torganization_id UUID NOT NULL, \n\tCONSTRAINT pk_crm_lead_activities PRIMARY KEY (id), \n\tCONSTRAINT uq_crm_activity_event UNIQUE (organization_id, event_key), \n\tCONSTRAINT fk_crm_lead_activities_lead_id_crm_leads FOREIGN KEY(lead_id) REFERENCES crm_leads (id) ON DELETE RESTRICT, \n\tCONSTRAINT fk_crm_lead_activities_organization_id_organizations FOREIGN KEY(organization_id) REFERENCES organizations (id) ON DELETE RESTRICT\n)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_crm_lead_activities_lead_id ON crm_lead_activities (lead_id)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_crm_lead_activities_organization_id ON crm_lead_activities (organization_id)')


def downgrade():
    raise RuntimeError('CRM contains contact history. Export and plan recovery before removing tables.')
