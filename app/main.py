import os
import logging
import time
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.auth.jwt_handler import (
    create_access_token, create_refresh_token, decode_token,
    get_password_hash, verify_password, validate_password, TokenPair
)
from app.roles.roles import Role
from app.permissions.permissions import Permission, has_permission

logger = logging.getLogger(__name__)

app = FastAPI(title="Secure Auth + RBAC Template", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

security = HTTPBearer()

login_attempts: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX_ATTEMPTS = 5

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    username: str
    role: Role

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: Role = Role.VIEWER

fake_users_db = {
    "admin": {"password": get_password_hash("Admin@123"), "role": Role.ADMIN},
    "editor": {"password": get_password_hash("Editor@123"), "role": Role.EDITOR},
    "viewer": {"password": get_password_hash("Viewer@123"), "role": Role.VIEWER},
}

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

setup_logging()

def check_rate_limit(username: str):
    now = time.time()
    attempts = login_attempts[username]
    attempts = [t for t in attempts if now - t < RATE_LIMIT_WINDOW]
    login_attempts[username] = attempts
    if len(attempts) >= RATE_LIMIT_MAX_ATTEMPTS:
        logger.warning("Rate limit exceeded for user: %s", username)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {RATE_LIMIT_WINDOW} seconds."
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
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
    return {"service": "Secure Auth + RBAC Template", "version": "1.1.0", "status": "running"}

@app.post("/auth/login")
def login(req: LoginRequest):
    check_rate_limit(req.username)
    user = fake_users_db.get(req.username)
    if not user or not verify_password(req.password, user["password"]):
        login_attempts[req.username].append(time.time())
        logger.warning("Failed login attempt for user: %s", req.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    login_attempts[req.username].clear()
    token_data = {"sub": req.username, "role": user["role"].value}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": req.username})
    logger.info("User logged in: %s", req.username)
    return TokenPair(access_token=access_token, refresh_token=refresh_token).model_dump()

@app.post("/auth/refresh")
def refresh(req: RefreshRequest):
    payload = decode_token(req.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    username = payload.get("sub")
    user = fake_users_db.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    token_data = {"sub": username, "role": user["role"].value}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": username})
    return TokenPair(access_token=access_token, refresh_token=refresh_token).model_dump()

@app.post("/auth/register")
def register(req: RegisterRequest):
    if req.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    try:
        validate_password(req.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    fake_users_db[req.username] = {
        "password": get_password_hash(req.password),
        "role": req.role,
    }
    logger.info("User registered: %s", req.username)
    return {"message": "User registered successfully", "username": req.username}

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
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
