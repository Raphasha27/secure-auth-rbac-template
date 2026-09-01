# Secure Auth & RBAC API — Documentation

> Role-Based Access Control system built with FastAPI — production-ready template for authentication, authorization, and fine-grained permission management.

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require a JWT Bearer token:

```
Authorization: Bearer <your-token>
```

## Roles & Permissions

| Role | Permissions |
|------|-------------|
| `user` | View content |
| `editor` | View + create content |
| `admin` | Full access (users, roles, content) |

Custom permissions follow the `resource:action` pattern: `content:write`, `content:delete`.

---

## Endpoints

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness probe |

### Auth

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive JWT |
| `GET` | `/auth/me` | Get current user profile *(auth required)* |

### Admin

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/admin/users` | List all users *(admin only)* |
| `POST` | `/admin/roles` | Create a role with permissions *(admin only)* |

### Content

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/content` | List content *(user/editor/admin role)* |
| `POST` | `/content` | Create content *(content:write permission)* |
| `DELETE` | `/content/{content_id}` | Delete content *(content:delete permission)* |

---

## Example Requests

### Register

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secureP@ss123",
    "full_name": "Jane Doe"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user"
}
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "secureP@ss123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### List Users (Admin)

```bash
curl http://localhost:8000/admin/users \
  -H "Authorization: Bearer <admin-token>"
```

### Create Role (Admin)

```bash
curl -X POST http://localhost:8000/admin/roles \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "editor",
    "permissions": ["content:write", "content:delete"]
  }'
```

### Create Content

```bash
curl -X POST http://localhost:8000/content \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Post",
    "body": "This is the content body."
  }'
```

### Delete Content

```bash
curl -X DELETE http://localhost:8000/content/1 \
  -H "Authorization: Bearer <token>"
```

---

## Error Responses

| Status | Meaning |
|--------|---------|
| `400` | Bad request (e.g., duplicate email) |
| `401` | Invalid credentials |
| `403` | Insufficient permissions (wrong role/permission) |
| `404` | Resource not found |

---

## Interactive Docs

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec:** [`docs/api-spec.yaml`](./api-spec.yaml)
