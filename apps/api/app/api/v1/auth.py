import hashlib
from datetime import UTC, datetime, timedelta
from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.dependencies import Auth, DB
from app.core.config import settings
from app.core.security import create_token, decode_token, verify_password
from app.models.identity import Membership, Organization, RefreshSession, User
from app.schemas.auth import CurrentUser, LoginRequest, RefreshRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["Autenticação"])
def digest(token: str) -> str: return hashlib.sha256(token.encode()).hexdigest()
def issue_pair(user_id: UUID, organization_id: UUID) -> TokenPair:
    return TokenPair(access_token=create_token(user_id, organization_id, "access", timedelta(minutes=settings.access_token_minutes)), refresh_token=create_token(user_id, organization_id, "refresh", timedelta(days=settings.refresh_token_days)))

@router.post("/login", response_model=TokenPair)
async def login(data: LoginRequest, db: DB) -> TokenPair:
    query = select(User, Organization).join(Membership, Membership.user_id == User.id).join(Organization, Organization.id == Membership.organization_id).where(User.email == data.email.lower(), Organization.slug == data.organization_slug, User.active.is_(True), Organization.active.is_(True), Membership.active.is_(True))
    row = (await db.execute(query)).one_or_none()
    if row is None or not verify_password(data.password, row.User.password_hash):
        raise HTTPException(status_code=401, detail="E-mail, senha ou organização inválidos.")
    pair = issue_pair(row.User.id, row.Organization.id)
    db.add(RefreshSession(user_id=row.User.id, organization_id=row.Organization.id, token_hash=digest(pair.refresh_token), expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_days)))
    await db.commit()
    return pair

@router.post("/refresh", response_model=TokenPair)
async def refresh(data: RefreshRequest, db: DB) -> TokenPair:
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh": raise ValueError
        user_id, organization_id = UUID(payload["sub"]), UUID(payload["org"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Refresh token inválido.") from exc
    session = (await db.execute(select(RefreshSession).where(RefreshSession.token_hash == digest(data.refresh_token), RefreshSession.revoked_at.is_(None), RefreshSession.expires_at > datetime.now(UTC)))).scalar_one_or_none()
    if session is None: raise HTTPException(status_code=401, detail="Sessão expirada ou revogada.")
    session.revoked_at = datetime.now(UTC)
    pair = issue_pair(user_id, organization_id)
    db.add(RefreshSession(user_id=user_id, organization_id=organization_id, token_hash=digest(pair.refresh_token), expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_days)))
    await db.commit()
    return pair

@router.get("/me", response_model=CurrentUser)
async def me(auth: Auth) -> CurrentUser:
    return CurrentUser(id=auth.user.id, organization_id=auth.organization_id, email=auth.user.email, full_name=auth.user.full_name, permissions=sorted(auth.permissions))

