# Secure Auth + RBAC Template

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![CI](https://github.com/Raphasha27/secure-auth-rbac-template/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/secure-auth-rbac-template/actions)

FastAPI-based secure authentication and role-based access control (RBAC) template with JWT tokens, role hierarchy, and granular permission management.

## Features

- **JWT Authentication** — Login endpoint issues signed JWT tokens using HS256
- **Role Hierarchy** — `admin > manager > editor > viewer` with numerical ranking
- **Permission System** — Fine-grained permissions (read, write, delete, admin) mapped to roles
- **Secure Password Hashing** — bcrypt via passlib for credential storage
- **Zero-Trust Ready** — Stateless auth with bearer token validation on every request

## Quick Start

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | Service info |
| GET | `/health` | No | Health check |
| POST | `/auth/login` | No | Login (returns JWT) |
| GET | `/auth/me` | Bearer | Current user info |
| GET | `/admin` | Admin | Admin-only panel |
| GET | `/write` | Write | Write-access resource |

### Login credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| editor | editor123 | editor |
| viewer | viewer123 | viewer |

## Project Structure

```
secure-auth-rbac-template/
├── app/
│   ├── auth/
│   │   └── jwt_handler.py    # JWT creation, decoding, password hashing
│   ├── roles/
│   │   └── roles.py          # Role enum and hierarchy
│   ├── permissions/
│   │   └── permissions.py    # Permission enum and access checks
│   └── main.py               # FastAPI app with routes
├── tests/
│   └── test_auth.py          # Test suite
├── .env.example              # Environment variables template
├── .pre-commit-config.yaml   # Pre-commit hooks
├── pyproject.toml            # Python packaging config
└── requirements.txt          # Dependencies
```

## Testing

```bash
pytest
```

## Pre-commit

```bash
pip install pre-commit
pre-commit install
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

© 2026 **Kirov Dynamics Technology** | Built by **Koketso Raphasha (Raphasha27)**
