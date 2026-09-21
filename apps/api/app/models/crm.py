from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TenantMixin, TimestampMixin, UUIDPrimaryKey


class Lead(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = 'crm_leads'
    __table_args__ = (UniqueConstraint('organization_id', 'instagram', name='uq_crm_lead_profile'),)
    name: Mapped[str] = mapped_column(String(160))
    instagram: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(160), default='')
    status: Mapped[str] = mapped_column(String(30), default='aguardando')
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
