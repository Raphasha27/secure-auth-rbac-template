from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.dependencies import get_current_user, require_permission, require_role
from app.models import User

router = APIRouter(prefix="/content", tags=["content"])


class ContentCreate(BaseModel):
    title: str
    body: str


@router.get("", dependencies=[Depends(require_role("user", "admin", "editor"))])
async def list_content():
    return {"items": []}


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("content:write"))])
async def create_content(req: ContentCreate, user: User = Depends(get_current_user)):
    return {"id": 1, "title": req.title, "body": req.body, "author": user.username}


@router.delete("/{content_id}", dependencies=[Depends(require_permission("content:delete"))])
async def delete_content(content_id: int):
    return {"deleted": content_id}
