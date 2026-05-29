from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.auth.jwt_handler import create_access_token, decode_token, get_password_hash, verify_password
from app.roles.roles import Role, role_has_access
from app.permissions.permissions import Permission, has_permission

app = FastAPI(title="Secure Auth + RBAC Template", version="1.0.0")
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    role: Role

fake_users_db = {
    "admin": {"password": get_password_hash("admin123"), "role": Role.ADMIN},
    "editor": {"password": get_password_hash("editor123"), "role": Role.EDITOR},
    "viewer": {"password": get_password_hash("viewer123"), "role": Role.VIEWER},
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

def require_permission(permission: Permission):
    def checker(user: dict = Depends(get_current_user)):
        user_role = Role(user.get("role", "viewer"))
        if not has_permission(user_role, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return checker

@app.get("/")
def root():
    return {"service": "Secure Auth + RBAC Template", "version": "1.0.0", "status": "running"}

@app.post("/auth/login")
def login(req: LoginRequest):
    user = fake_users_db.get(req.username)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": req.username, "role": user["role"].value})
    return {"access_token": token, "token_type": "bearer", "role": user["role"].value}

@app.get("/auth/me", response_model=UserResponse)
def me(user: dict = Depends(get_current_user)):
    return UserResponse(username=user["sub"], role=Role(user["role"]))

@app.get("/admin")
def admin_panel(user: dict = Depends(require_permission(Permission.ADMIN))):
    return {"message": "Welcome, admin", "user": user["sub"]}

@app.get("/write")
def write_resource(user: dict = Depends(require_permission(Permission.WRITE))):
    return {"message": "Write access granted", "user": user["sub"]}

@app.get("/health")
def health():
    return {"status": "healthy"}
