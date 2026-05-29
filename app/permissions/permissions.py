from enum import Enum
from app.roles.roles import Role, role_has_access

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

PERMISSION_ROLES = {
    Permission.READ: [Role.VIEWER, Role.EDITOR, Role.MANAGER, Role.ADMIN],
    Permission.WRITE: [Role.EDITOR, Role.MANAGER, Role.ADMIN],
    Permission.DELETE: [Role.MANAGER, Role.ADMIN],
    Permission.ADMIN: [Role.ADMIN],
}

def has_permission(user_role: Role, required_permission: Permission) -> bool:
    allowed_roles = PERMISSION_ROLES.get(required_permission, [])
    return user_role in allowed_roles
