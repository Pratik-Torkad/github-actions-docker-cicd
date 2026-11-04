# Security Policy

## Reporting

Do not publish credentials, tokens, private keys, or sensitive logs in issues. If you discover a security issue in this learning project, contact the repository owner privately.

## Project safeguards

- The container runs as a non-root user.
- Local environment files, private keys, and Python virtual environments are excluded from the build context and Git.
- GitHub Actions uses read-only repository permissions for validation and grants package-write permission only to the main-branch publishing job.
- Pull requests run tests, a Docker build, and vulnerability scanning but cannot publish an image.
- Trivy is configured to fail on HIGH and CRITICAL vulnerabilities that it reports. Review the scan logs and do not treat ignored unfixed findings as resolved.

This repository is a portfolio learning example, not a production-certified service.
