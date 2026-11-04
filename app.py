"""Small Flask service used to demonstrate a GitHub Actions CI/CD pipeline."""

from flask import Flask, jsonify


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            service="flask-cicd-demo",
            status="running",
            message="Hello from the GitHub Actions and Docker CI/CD demo!",
        )

    @app.get("/health")
    def health():
        """Return a simple health response for Docker and orchestrators."""
        return jsonify(status="healthy"), 200

    return app


app = create_app()
