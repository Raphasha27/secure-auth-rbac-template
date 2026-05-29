from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EDITOR = "editor"
    VIEWER = "viewer"

ROLE_HIERARCHY = {
    Role.ADMIN: 100,
    Role.MANAGER: 80,
    Role.EDITOR: 50,
    Role.VIEWER: 10,
}

def role_has_access(required_role: Role, user_role: Role) -> bool:
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)
