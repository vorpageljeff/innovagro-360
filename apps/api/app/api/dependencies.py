from dataclasses import dataclass
from typing import Annotated
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.db.session import get_db
from app.models.identity import Membership, User

bearer = HTTPBearer(auto_error=False)
DB = Annotated[AsyncSession, Depends(get_db)]

@dataclass(frozen=True)
class AuthContext:
    user: User
    organization_id: UUID
    permissions: frozenset[str]

async def get_auth_context(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], db: DB) -> AuthContext:
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida.")
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access": raise unauthorized
        user_id, organization_id = UUID(payload["sub"]), UUID(payload["org"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise unauthorized from exc
    membership = (await db.execute(select(Membership).where(Membership.user_id == user_id, Membership.organization_id == organization_id, Membership.active.is_(True)))).scalar_one_or_none()
    user = await db.get(User, user_id)
    if not membership or not user or not user.active: raise unauthorized
    permissions = frozenset(p.key for role in membership.roles for p in role.permissions)
    return AuthContext(user, organization_id, permissions)

Auth = Annotated[AuthContext, Depends(get_auth_context)]

def require_permission(permission: str):
    async def dependency(auth: Auth) -> AuthContext:
        if permission not in auth.permissions:
            raise HTTPException(status_code=403, detail="Você não tem permissão para esta ação.")
        return auth
    return dependency

