from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.models import Permission, Role, User

router = APIRouter(prefix="/admin", tags=["admin"])


class RoleAssignRequest(BaseModel):
    name: str
    permissions: list[str] = []


@router.get("/users")
async def list_users(
    _admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"id": u.id, "email": u.email, "username": u.username} for u in users]


@router.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_role(
    req: RoleAssignRequest,
    _admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    existing = await db.execute(select(Role).where(Role.name == req.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(name=req.name)
    for perm_name in req.permissions:
        perm = (await db.execute(select(Permission).where(Permission.name == perm_name))).scalar_one_or_none()
        if not perm:
            perm = Permission(name=perm_name)
            db.add(perm)
            await db.flush()
        role.permissions.append(perm)

    db.add(role)
    await db.flush()
    return {"id": role.id, "name": role.name, "permissions": req.permissions}
