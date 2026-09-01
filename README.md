<div align="center">

# Secure Auth + RBAC Template

**Production-Ready Authentication & Role-Based Access Control Template for FastAPI**

[![CI](https://github.com/Raphasha27/secure-auth-rbac-template/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/secure-auth-rbac-template/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-4B2E83)](https://docs.astral.sh/ruff/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-95%25-brightgreen)](https://github.com/Raphasha27/secure-auth-rbac-template)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://github.com/Raphasha27/secure-auth-rbac-template)

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![Security](https://img.shields.io/badge/Security-JWT%20%2B%20RBAC-red?style=for-the-badge)

</div>

---

## Features

- **JWT Authentication** — Secure token generation and validation with refresh tokens
- **Role-Based Access Control** — Flexible `@require_role` decorator for endpoint protection
- **Password Hashing** — Bcrypt integration via passlib for secure credential storage
- **Admin / Moderator / USER Roles** — Predefined role hierarchy with granular permissions
- **Dependency Injection** — Clean FastAPI dependency pattern for auth and authorization
- **Token Refresh** — Automatic token rotation with configurable expiry
- **Template Ready** — Copy-paste starter for any FastAPI project

---

## Quick Start

```bash
git clone https://github.com/Raphasha27/secure-auth-rbac-template.git
cd secure-auth-rbac-template
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs (Swagger UI): `http://localhost:8000/docs`

---

## Architecture

> Full architecture documentation: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Client     │──────▶│   FastAPI    │──────▶│  PostgreSQL   │
│  (App)       │  HTTP │   (Auth +    │  SQL  │  (Users +     │
│              │◀──────│   RBAC)      │◀──────│   Roles)      │
└──────────────┘       └──────┬───────┘       └──────────────┘
                              │
                     ┌────────▼────────┐
                     │  JWT Tokens     │
                     │  (Access +      │
                     │   Refresh)      │
                     └─────────────────┘
```

---

## API Documentation

> Full API reference: [docs/API.md](docs/API.md) · Swagger UI: `http://localhost:8000/docs`

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register a new user | None |
| POST | `/api/v1/auth/login` | Login and receive JWT | None |
| POST | `/api/v1/auth/refresh` | Refresh access token | Refresh Token |
| GET | `/api/v1/auth/me` | Get current user profile | Bearer |

### Protected (Role-Based)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/admin/users` | List all users | ADMIN |
| POST | `/mod/content` | Create moderator content | ADMIN, MODERATOR |
| GET | `/user/profile` | View user profile | Any role |

---

## Usage Example

```python
from fastapi import Depends, FastAPI
from app.dependencies.rbac import require_role, Role

app = FastAPI()


# Only ADMINs can access this endpoint
@app.get("/admin/users", dependencies=[Depends(require_role([Role.ADMIN]))])
async def get_all_users():
    return {"users": [...]}


# ADMIN and MODERATOR can access
@app.post("/mod/content", dependencies=[Depends(require_role([Role.ADMIN, Role.MODERATOR]))])
async def create_content():
    return {"created": True}
```

---

## Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| Language | Python 3.11 | Core runtime |
| Framework | FastAPI | Async web framework |
| Auth | python-jose (JWT) | Stateless token authentication |
| Passwords | passlib + bcrypt | Secure password hashing |
| ORM | SQLAlchemy 2.0 | Database operations |
| Database | PostgreSQL | User and role storage |
| Validation | Pydantic v2 | Request/response schemas |
| Testing | pytest | Unit and integration tests |

---

## Project Structure

```
secure-auth-rbac-template/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── config.py              # Settings (JWT expiry, DB URL)
│   ├── models.py              # SQLAlchemy User/Role models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT token creation/validation
│   │   └── rbac.py            # @require_role decorator
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # Registration, login, refresh
│       └── admin.py           # Admin-only endpoints
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_auth.py           # Auth flow tests
│   └── test_rbac.py           # Role-based access tests
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

---

## Testing

```bash
pip install -r requirements.txt
pytest --cov=app --cov-report=term-missing -v
```

---

## Deployment

### Docker

```bash
docker-compose up --build -d
docker-compose logs -f       # View live logs
docker-compose down           # Stop all services
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET_KEY` | — | Secret for JWT signing (required) |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token expiry |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token expiry |
| `DATABASE_URL` | `sqlite:///./test.db` | Database connection string |
| `BCRYPT_ROUNDS` | `12` | Bcrypt hashing rounds |

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built by <a href="https://github.com/Raphasha27">Koketso Raphasha</a> · <a href="https://portfolio-iota-eight-90.vercel.app/">Portfolio</a>
</div>
