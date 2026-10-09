from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TenantMixin, TimestampMixin, UUIDPrimaryKey


class Lead(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_leads'
    __table_args__ = (UniqueConstraint('organization_id', 'instagram', name='uq_crm_lead_profile'), Index('uq_crm_lead_phone', 'organization_id', 'phone', unique=True))
    name: Mapped[str] = mapped_column(String(160))
    instagram: Mapped[str | None] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(160), default='')
    status: Mapped[str] = mapped_column(String(30), default='aguardando')
    priority: Mapped[str] = mapped_column(String(10), default='media', server_default='media')
    phone: Mapped[str | None] = mapped_column(String(16))
    bot_paused: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
    last_contact_on: Mapped[date | None] = mapped_column(Date)
    next_contact_on: Mapped[date | None] = mapped_column(Date)


class LeadActivity(UUIDPrimaryKey, TenantMixin, Base):
    __tablename__ = 'crm_lead_activities'
    __table_args__ = (UniqueConstraint('organization_id', 'event_key', name='uq_crm_activity_event'),)
    lead_id: Mapped[UUID] = mapped_column(ForeignKey('crm_leads.id', ondelete='RESTRICT'), index=True)
    event_key: Mapped[str] = mapped_column(String(120))
    kind: Mapped[str] = mapped_column(String(20))
    requested_status: Mapped[str | None] = mapped_column(String(30))
    requested_next_contact_on: Mapped[date | None] = mapped_column(Date)
    occurred_on: Mapped[date] = mapped_column(Date)
    note: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AutomationRule(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_automation_rules'
    name: Mapped[str] = mapped_column(String(120))
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    position: Mapped[int] = mapped_column(Integer, default=100, server_default='100')
    handoff: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
    contains: Mapped[str] = mapped_column(String(200), default='')
    reply: Mapped[str] = mapped_column(Text, default='')
    priority: Mapped[str | None] = mapped_column(String(10))
    status: Mapped[str | None] = mapped_column(String(30))


class AutomationReceipt(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_automation_receipts'
    __table_args__ = (UniqueConstraint('organization_id', 'message_id', name='uq_crm_webhook_message'),)
    message_id: Mapped[str] = mapped_column(String(200))
    lead_id: Mapped[UUID | None] = mapped_column(ForeignKey('crm_leads.id', ondelete='RESTRICT'))
    incoming: Mapped[str] = mapped_column(Text)
    reply: Mapped[str] = mapped_column(Text, default='')
    state: Mapped[str] = mapped_column(String(30), default='received')


class InstagramMessage(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_instagram_messages'
    __table_args__ = (
        UniqueConstraint('organization_id', 'message_id', name='uq_crm_instagram_message'),
    )
    message_id: Mapped[str] = mapped_column(String(200))
    lead_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('crm_leads.id', ondelete='RESTRICT'), index=True
    )
    instagram_scoped_user_id: Mapped[str] = mapped_column(String(64), index=True)
    username: Mapped[str | None] = mapped_column(String(30), index=True)
    direction: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(Text, default='')
    attachment_type: Mapped[str | None] = mapped_column(String(30))
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
