# Contributing to Secure Auth + RBAC Template

Welcome and thank you for your interest in contributing to **Secure Auth + RBAC Template**! Every contribution helps make authentication and authorization better for FastAPI projects.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Architecture Reference](#architecture-reference)
- [Release Process](#release-process)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to **raphasha27@github.com**.

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Runtime |
| pip | Latest | Dependency management |
| Docker | 24.x+ | Optional containerized development |

### Step-by-Step Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/<your-username>/secure-auth-rbac-template.git
   cd secure-auth-rbac-template
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

5. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Verify the API**:
   - Swagger UI: `http://localhost:8000/docs`

7. **Run linter locally** (optional):
   ```bash
   ruff check .
   ruff format .
   ```

---

## Code Style Guidelines

### Python (FastAPI)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide.
- Use **Ruff** for linting and formatting — CI enforces this.
- Maximum line length: **88 characters**.
- Use type hints on all function signatures.
- Prefer async/await for I/O-bound operations.

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` | `create_user` |
| Classes | `PascalCase` | `UserService` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_ROLE` |
| API routes | `kebab-case` | `/api/v1/auth/login` |
| Database columns | `snake_case` | `created_at` |

### Security-Specific Guidelines

- **Never** log JWT tokens or passwords.
- Use bcrypt with proper cost factors for password hashing.
- Validate JWT signatures on every protected endpoint.
- Implement proper token expiry and refresh rotation.
- Use parameterized queries — never string interpolation for SQL.

### General

- Write meaningful variable and function names.
- Add docstrings for all public functions and classes.
- Keep functions focused and under 40 lines.
- No hardcoded secrets — use environment variables.

---

## Testing Requirements

| Type | Framework | Coverage Target |
|------|-----------|-----------------|
| Unit tests | pytest | 90%+ |
| Auth tests | pytest + httpx | 95%+ |
| RBAC tests | pytest | All role combinations |

- Every new feature **must** include tests.
- Bug fixes **must** include a regression test.
- Run the full test suite before pushing:
  ```bash
  pytest tests/ -v --cov=app --cov-report=term-missing
  ```
- Test all role combinations (admin, moderator, user) for RBAC changes.

---

## Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines above.

3. **Write or update tests** to cover your changes.

4. **Commit with a conventional message**:
   ```
   feat: add API key authentication
   fix: correct token refresh edge case
   docs: update RBAC middleware documentation
   test: add tests for role-based endpoint access
   chore: update security dependencies
   ```

5. **Push and open a PR** against `main`.

6. **PR checklist** (all must pass before merge):
   - [ ] CI pipeline passes (linting, tests)
   - [ ] Code reviewed by at least one maintainer
   - [ ] No merge conflicts with `main`
   - [ ] Security review completed (for auth/RBAC changes)
   - [ ] Documentation updated (if applicable)
   - [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## Issue Guidelines

### Bug Reports

- Check [existing issues](../../issues) first to avoid duplicates.
- Include a clear, descriptive title.
- Provide steps to reproduce, expected vs. actual behavior.
- Include environment details: Python version, FastAPI version, OS.
- Attach error logs if relevant.

### Feature Requests

- Describe the feature and its motivation.
- Explain the use case for authentication/authorization.
- Propose an implementation approach if possible.

### Security Issues

- **Do not** open public issues for security vulnerabilities.
- Follow the security reporting process in [SECURITY.md](SECURITY.md).

### Labels

| Label | Description |
|-------|-------------|
| `bug` | Something is broken |
| `enhancement` | New feature or improvement |
| `good-first-issue` | Ideal for first-time contributors |
| `security` | Security-related concern |
| `help-wanted` | Community help appreciated |

---

## Architecture Reference

For detailed system design, data flow diagrams, and component interactions, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Key components to understand:
- **FastAPI Auth** — JWT token generation, validation, and refresh
- **RBAC Middleware** — Role-based access control with `@require_role` decorator
- **Password Hashing** — Bcrypt integration via passlib
- **PostgreSQL** — User and role storage with async SQLAlchemy

---

## Release Process

1. All changes merge to `main` via PR with passing CI.
2. Semantic versioning is used: `MAJOR.MINOR.PATCH`.
3. Tags are created for each release: `git tag v1.x.x`.
4. Release notes are generated from conventional commit messages.

---

## Questions?

Open a [discussion](../../discussions) or reach out to **raphasha27@github.com**.

Thank you for contributing to Secure Auth + RBAC Template!
