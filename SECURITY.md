# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | :white_check_mark: Active |
| < Latest | :x: No |

Always use the latest version to receive security patches and improvements.

---

## Reporting a Vulnerability

The Secure Auth + RBAC Template team takes security seriously — this is a security-focused template. We appreciate your efforts to responsibly disclose any security concerns.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### Step-by-Step Reporting Process

1. **Identify the vulnerability** — Document the issue with clear reproduction steps.
2. **Email the security team** at **raphasha27@github.com** with the following:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
3. **Wait for acknowledgment** — You will receive a response within **48 hours**.
4. **Collaborate on the fix** — We may reach out for additional details.
5. **Disclosure** — We will coordinate a public disclosure timeline with you.

### What to Include

- Type of vulnerability (e.g., JWT bypass, privilege escalation, timing attack)
- Affected component and version
- Attack vector and prerequisites
- Proof of concept (if available)
- Your suggested remediation

---

## Security Response Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial acknowledgment | 48 hours |
| Severity assessment | 3 business days |
| Patch development | 5–10 business days |
| Coordinated disclosure | 30 days after fix |

Authentication bypass or privilege escalation vulnerabilities may receive expedited timelines.

---

## Security Design

This project implements the following security measures:

- **JWT Authentication** — Stateless tokens with RS256/HS256 signing
- **Refresh Token Rotation** — Automatic token rotation on each use
- **Bcrypt Password Hashing** — Secure credential storage with configurable cost
- **RBAC Authorization** — Granular role-based access control
- **Rate Limiting** — Protection against brute force attacks
- **Input Validation** — Pydantic models validate all API inputs
- **SQL Injection Protection** — SQLAlchemy ORM with parameterized queries
- **CORS Configuration** — Restricted to trusted origins
- **Environment Variables** — No hardcoded secrets

---

## Security Bestactices for Users

When using this template in your project:

### JWT Configuration
- Use **RS256** (asymmetric) for production — HS256 requires shared secret management
- Set short access token expiry (15 minutes recommended)
- Implement refresh token rotation with database tracking
- Store tokens securely — HttpOnly cookies for web apps, secure storage for mobile

### Password Security
- Enforce minimum password length (12+ characters recommended)
- Use bcrypt with cost factor 12+ (not lower)
- Implement account lockout after failed attempts
- Consider adding MFA for sensitive applications

### Role-Based Access
- Follow the principle of least privilege
- Validate roles on every protected endpoint
- Audit role changes and permission grants
- Use hierarchical roles where possible

### Environment Security
- Never commit `.env` files or secrets to version control
- Use Docker secrets or a vault service for production
- Rotate JWT signing keys periodically
- Monitor for unusual authentication patterns

### Network
- Deploy behind a reverse proxy with TLS termination
- Enable CORS only for trusted frontend origins
- Use HTTPS for all API communications
- Implement security headers (HSTS, CSP, etc.)

### Dependencies
- Run `pip audit` for Python dependency vulnerabilities
- Enable Dependabot alerts for automatic vulnerability notifications
- Review dependency updates before merging

---

## Dependency Management

### Python Dependencies

```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Automated Scanning

- **Dependabot** is enabled for automatic dependency update PRs.
- **CI pipeline** runs `pip-audit` on every PR.
- Review and merge Dependabot PRs promptly.
- Pay special attention to security library updates (bcrypt, passlib, python-jose).

---

## Responsible Disclosure

We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) principles:

- Report vulnerabilities privately before public disclosure.
- We will credit reporters in release notes (unless anonymity is preferred).
- We ask that you do not exploit the vulnerability beyond what is necessary to demonstrate it.
- We will not pursue legal action against researchers who follow this policy.

---

## Contact

- **Security Email**: raphasha27@github.com
- **General Issues**: [GitHub Issues](../../issues)

Thank you for helping keep Secure Auth + RBAC Template and its users safe.
