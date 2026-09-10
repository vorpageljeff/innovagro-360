from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    organization_slug: str = Field(min_length=2, max_length=80)

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CurrentUser(BaseModel):
    id: UUID
    organization_id: UUID
    email: EmailStr
    full_name: str
    permissions: list[str]

