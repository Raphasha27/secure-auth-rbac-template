"""Secure Auth RBAC Template — FastAPI application with role-based access control."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import Base
from app.routers import admin, auth, content

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Create database tables on startup for development."""
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Secure Auth & RBAC API",
    description=(
        "Role-Based Access Control (RBAC) system built with FastAPI — a production-ready template "
        "for authentication, authorization, and fine-grained permission management.\n\n"
        "## Features\n"
        "- **Authentication** — Register and login with JWT tokens\n"
        "- **Role Management** — Create roles and assign permissions (admin only)\n"
        "- **Content Management** — CRUD operations with role/permission guards\n"
        "- **Access Control** — Enforce `require_role` and `require_permission` dependencies\n\n"
        "## Roles & Permissions\n"
        "Built-in roles: `user`, `admin`, `editor`. Custom roles can be created via the admin panel.\n"
        "Permissions follow the `resource:action` pattern (e.g. `content:write`, `content:delete`)."
    ),
    version="2.0.0",
    contact={
        "name": "Secure Auth RBAC Support",
        "url": "https://github.com/Raphasha27/secure-auth-rbac-template",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "auth", "description": "User registration, login, and profile management"},
        {"name": "admin", "description": "Administrative operations — user listing and role management"},
        {"name": "content", "description": "Content CRUD with role and permission-based access control"},
        {"name": "Health", "description": "Service liveness probes"},
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(content.router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Liveness probe endpoint."""
    return {"status": "ok", "service": "rbac-api"}
