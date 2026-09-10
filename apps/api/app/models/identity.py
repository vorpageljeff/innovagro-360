from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TenantMixin, TimestampMixin, UUIDPrimaryKey

role_permissions = Table("role_permissions", Base.metadata,
    Column("role_id", PGUUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", PGUUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True))
membership_roles = Table("membership_roles", Base.metadata,
    Column("membership_id", PGUUID(as_uuid=True), ForeignKey("memberships.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", PGUUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True))


class Organization(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "organizations"
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class User(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    password_hash: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Membership(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = "memberships"
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles: Mapped[list["Role"]] = relationship(secondary=membership_roles, lazy="selectin")


class Permission(UUIDPrimaryKey, Base):
    __tablename__ = "permissions"
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(240))


class Role(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("organization_id", "name"),)
    name: Mapped[str] = mapped_column(String(80))
    permissions: Mapped[list[Permission]] = relationship(secondary=role_permissions, lazy="selectin")


class RefreshSession(UUIDPrimaryKey, TimestampMixin, TenantMixin, Base):
    __tablename__ = "refresh_sessions"
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AuditLog(UUIDPrimaryKey, TenantMixin, Base):
    __tablename__ = "audit_logs"
    user_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    entity: Mapped[str] = mapped_column(String(80), index=True)
    entity_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True), index=True, nullable=True)
    before: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    after: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
