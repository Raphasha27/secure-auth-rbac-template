# Secure Auth + RBAC Template — Architecture

## System Overview

A production-ready, reusable authentication and Role-Based Access Control (RBAC) template built with FastAPI. Implements JWT authentication, decorator-based role enforcement (ADMIN, MODERATOR, USER), and bcrypt password hashing — designed as a copy-paste starting point for any FastAPI project needing auth.

## Architecture Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   Client     │──────►│   FastAPI        │──────►│  SQLite/     │
│  (Any HTTP)  │  JWT  │   (Python 3.11)  │  SQL  │  PostgreSQL  │
│              │◄──────│                  │◄──────│              │
└──────────────┘       └───────┬──────────┘       └──────────────┘
                               │
                      ┌────────▼────────┐
                      │  RBAC Middleware │
                      │  @require_role  │
                      │  Role enum check│
                      └─────────────────┘
```

## Technology Stack

| Component      | Technology            | Version |
|----------------|-----------------------|---------|
| Language       | Python                | 3.11    |
| Framework      | FastAPI               | 0.115   |
| Auth           | JWT (python-jose)     | —       |
| Password Hash  | bcrypt (passlib)      | —       |
| ORM            | SQLAlchemy            | —       |
| Validation     | Pydantic              | —       |
| Testing        | pytest                | —       |
| Linting        | ruff                  | —       |
| CI/CD          | GitHub Actions        | —       |

## Directory Structure

```
secure-auth-rbac-template/
├── app/
│   ├── config.py              # Settings (SECRET_KEY, DB URL, token expiry)
│   ├── main.py                # FastAPI app factory
│   ├── models.py              # SQLAlchemy User model
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── rbac.py            # require_role(), Role enum, get_current_user()
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # POST /register, /login, GET /me
│       ├── admin.py           # Admin-only endpoints (role-gated)
│       └── content.py         # Example content endpoints
├── tests/
├── frontend/                  # Optional reference frontend
├── docs/
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Data Flow

### Registration
1. Client sends `POST /register` with email + password.
2. Password hashed with bcrypt (12 rounds).
3. User created with default role `USER`.
4. Returns success confirmation.

### Authentication
1. Client sends `POST /login` with credentials.
2. System verifies bcrypt hash, generates JWT with `sub` (user_id) and `role` claims.
3. Token returned with configurable expiry.

### Authorization (RBAC)
1. Protected endpoint declares required roles: `dependencies=[Depends(require_role([Role.ADMIN]))]`
2. `require_role()` dependency extracts JWT from `Authorization: Bearer` header.
3. Decodes token, checks `role` claim against allowed roles.
4. Returns 403 Forbidden if role not matched.

### Role Hierarchy

```
ADMIN > MODERATOR > USER
```

- **ADMIN**: Full access — user management, system config, all endpoints.
- **MODERATOR**: Content moderation — manage content, view users.
- **USER**: Basic access — own profile, read content.

## Security

- **JWT Tokens**: Stateless auth; tokens signed with HS256 using `SECRET_KEY`.
- **Password Hashing**: bcrypt with passlib — 12 rounds, resistant to rainbow tables.
- **Role Enforcement**: Decorator-based `@require_role()` — fail-closed (denies by default).
- **Token Expiry**: Configurable `ACCESS_TOKEN_EXPIRE_MINUTES` — short-lived tokens.
- **CORS**: Restrict to known origins in production.
- **No secrets in code**: `SECRET_KEY` loaded from environment variable.
- **SQL Injection**: SQLAlchemy ORM prevents injection; no raw SQL.

## Deployment

### Docker

```bash
docker-compose up --build
```

### Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables

| Variable              | Description                      |
|-----------------------|----------------------------------|
| `SECRET_KEY`          | JWT signing secret (required)    |
| `DATABASE_URL`        | SQLAlchemy database URL          |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry (default: 30) |

### Usage as Template

```python
from app.dependencies.rbac import require_role, Role


@app.get("/admin/users", dependencies=[Depends(require_role([Role.ADMIN]))])
async def get_all_users():
    return {"users": [...]}
```

## Scaling Considerations

- **Token storage**: Use HTTP-only cookies or secure mobile storage; avoid localStorage.
- **Refresh tokens**: Implement refresh token rotation for long-lived sessions.
- **Rate limiting**: Add per-endpoint rate limiting to prevent brute-force attacks.
- **Database**: Swap SQLite for PostgreSQL in production; use connection pooling.
- **Multi-tenancy**: Extend Role enum with tenant-scoped roles; add tenant_id to JWT claims.
- **Session revocation**: Add Redis-based token blacklist for immediate logout.

## Decision Records

| Decision | Rationale |
|----------|-----------|
| Decorator-based RBAC | Python-native, explicit at endpoint level — no magic, easy to audit |
| JWT over sessions | Stateless scales horizontally; no shared session store needed |
| Role enum over DB roles | Compile-time safety; roles are application constants, not user-configurable |
| bcrypt over argon2 | More widely supported in Python ecosystem; 12 rounds is sufficient |
| FastAPI Depends | Framework-native DI — clean, testable, composable |
| Single-file RBAC | `rbac.py` is self-contained — copy one file to reuse in any FastAPI project |
