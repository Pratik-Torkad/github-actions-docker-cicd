# GitHub Actions + Docker CI/CD Pipeline

A hands-on DevOps portfolio project demonstrating an automated CI/CD workflow for a small Python Flask service.

> **Project status:** Initial implementation committed. CI execution and container publication must be confirmed in the GitHub Actions tab before describing the pipeline as passing or deployed.

## What this project demonstrates

- A small HTTP service with health endpoint.
- Automated unit tests with pytest.
- A non-root Docker image with a container health check.
- GitHub Actions CI on pushes and pull requests.
- Docker image vulnerability scanning with Trivy.
- Container image publication to GitHub Container Registry (GHCR) from the `main` branch only.
- Image SBOM and provenance generation through BuildKit.

## Pipeline

```text
Pull request / push to main
          |
          v
  Install Python dependencies
          |
          v
     Run pytest suite
          |
          v
     Build Docker image
          |
          v
   Trivy vulnerability scan
          |
          +---- pull request: stop (no image publication)
          |
          +---- push to main: publish to GHCR
                                |
                                v
                       SHA tag + latest tag
                       SBOM + provenance
```

## Repository layout

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci-cd.yml
├── tests/
│   └── test_app.py
├── .dockerignore
├── .gitignore
├── app.py
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── SECURITY.md
```

## Run locally (Windows PowerShell)

1. Install Python 3.12+ and Docker Desktop.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies and run tests:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt
   pytest -v
   ```

4. Start the service:

   ```powershell
   python -m flask --app app run --host 0.0.0.0 --port 5000
   ```

5. Open `http://localhost:5000/` and `http://localhost:5000/health`.

## Run with Docker

Build and start:

```bash
docker build -t flask-cicd-demo:local .
docker run --rm -p 5000:5000 flask-cicd-demo:local
```

Or use Docker Compose:

```bash
docker compose up --build
docker compose down
```

The service listens on port 5000. The container health check calls `/health`.

## CI/CD behavior

The workflow at `.github/workflows/ci-cd.yml` runs for pull requests targeting `main`, pushes to `main`, and manual dispatch.

1. **Test:** installs development dependencies and runs pytest.
2. **Build and scan:** builds the Docker image and scans it with Trivy for HIGH and CRITICAL vulnerabilities. Unfixed findings are ignored by the configured scanner input; review scanner output rather than assuming a clean image.
3. **Publish:** only a push to `main` can publish the image to GHCR. Pull requests never receive package-write permissions and never publish images.

The workflow uses the repository's built-in `GITHUB_TOKEN`; no Docker Hub password or personal access token is required. The publish job requests only `contents: read` and `packages: write`.

## Container image

The workflow publishes:

```text
ghcr.io/pratik-torkad/flask-cicd-demo:latest
ghcr.io/pratik-torkad/flask-cicd-demo:sha-<commit>
```

After the first successful publication, check the package under your GitHub profile's **Packages** tab. GHCR packages may initially be private; review the package visibility settings before sharing the image publicly.

Pull and run (after publication):

```bash
docker pull ghcr.io/pratik-torkad/flask-cicd-demo:latest
docker run --rm -p 5000:5000 ghcr.io/pratik-torkad/flask-cicd-demo:latest
```

## Troubleshooting

- Open **Actions** in the repository to inspect each job and its logs.
- If package publication fails with a permissions error, check repository Actions permissions and the GHCR package's access settings.
- If Trivy finds HIGH or CRITICAL vulnerabilities, review the package, base-image and OS findings; update dependencies or the base image and rerun the workflow. Do not suppress findings without understanding them.
- If Docker is unavailable locally, the GitHub-hosted runner can still build and scan the image.

## Portfolio completion checklist

- [ ] GitHub Actions test job passes.
- [ ] Docker build job passes.
- [ ] Trivy scan output reviewed and findings addressed or documented.
- [ ] Main-branch image successfully published to GHCR.
- [ ] Pull the published image and verify `/` and `/health`.
- [ ] Add genuine screenshots and workflow run links.

Do not claim a successful deployment or a passed security scan until the corresponding run and image have been verified.
