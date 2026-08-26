[![CI](https://github.com/Raphasha27/secure-auth-rbac-template/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/secure-auth-rbac-template/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🔐 Secure Auth + RBAC Template

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![Security](https://img.shields.io/badge/Security-JWT%20%2B%20RBAC-red?style=for-the-badge)

A production-ready, reusable authentication and Role-Based Access Control (RBAC) template built with FastAPI.

## Why use this template?
Most tutorials only show basic JWT login. This template implements a flexible, decorator-based RBAC system allowing you to secure endpoints based on user roles (ADMIN, MODERATOR, USER).

## Core Features
- **JWT Authentication:** Secure token generation and validation.
- **Role-Based Access Control:** Highly flexible @require_role dependency injection.
- **Password Hashing:** Bcrypt integration via passlib.

## Usage Example
`python
from app.dependencies.rbac import require_role, Role

# Only ADMINs can access this endpoint
@app.get("/admin/users", dependencies=[Depends(require_role([Role.ADMIN]))])
async def get_all_users():
    return {"users": [...]}
`
