from fastapi import Depends, HTTPException, status


class Role:
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


# Mock user dependency
async def get_current_user():
    return {"id": 1, "username": "testuser", "role": Role.USER}


def require_role(allowed_roles: list[str]):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this action"
            )
        return current_user

    return role_checker
