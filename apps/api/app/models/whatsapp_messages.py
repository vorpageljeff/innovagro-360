from uuid import UUID
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TenantMixin, TimestampMixin, UUIDPrimaryKey

class WhatsAppDraft(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_whatsapp_drafts'
    __table_args__ = (UniqueConstraint('organization_id', 'lead_id', name='uq_whatsapp_draft_lead'),)
    lead_id: Mapped[UUID | None] = mapped_column(ForeignKey('crm_leads.id', ondelete='RESTRICT'))
    text: Mapped[str] = mapped_column(Text)
    request_id: Mapped[UUID] = mapped_column()

class WhatsAppOutbound(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_whatsapp_outbound'
    __table_args__ = (UniqueConstraint('organization_id', 'request_id', name='uq_whatsapp_outbound_request'),)
    lead_id: Mapped[UUID] = mapped_column(ForeignKey('crm_leads.id', ondelete='RESTRICT'), index=True)
    request_id: Mapped[UUID] = mapped_column()
    phone: Mapped[str] = mapped_column(String(16))
    text: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(20))

class WhatsAppRead(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_whatsapp_reads'
    __table_args__ = (UniqueConstraint('organization_id', 'user_id', 'receipt_id', name='uq_whatsapp_read_user_receipt'),)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'))
    lead_id: Mapped[UUID] = mapped_column(ForeignKey('crm_leads.id', ondelete='RESTRICT'), index=True)
    receipt_id: Mapped[UUID] = mapped_column(ForeignKey('crm_automation_receipts.id', ondelete='RESTRICT'))
