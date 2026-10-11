# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | ✅ |

## Reporting a Vulnerability

Please do **not** report security vulnerabilities through public GitHub issues.

To report a security vulnerability:

1. Email the maintainers at the address listed in the repository's GitHub profile (or open a GitHub Security Advisory).
2. Include a description of the vulnerability, steps to reproduce it, and its potential impact.
3. Allow reasonable time for a response and fix before any public disclosure.

We will acknowledge receipt within 72 hours and aim to resolve critical issues within 14 days.

## Security Principles

- Secrets are stored in environment variables only — never committed to the repository.
- Private keys (including blockchain signing keys) are never exposed in client-side code.
- Source content retrieved from external URLs is treated as untrusted input.
- Database queries use parameterised statements to prevent SQL injection.
- SSRF protections block requests to loopback, private, and cloud metadata addresses.
- No personal data is stored on-chain.

## Out of Scope

- Vulnerabilities in third-party dependencies (please report to their respective maintainers).
- Issues that require physical access to a device.
