"""Flask application for SDR Agent web interface."""

import sys
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from flask import Flask  # noqa: E402
from flask_cors import CORS  # noqa: E402

from sdr_agent.config import get_settings  # noqa: E402


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Store settings in app config
    try:
        settings = get_settings()
        app.config["settings"] = settings
    except Exception as e:
        print(f"Warning: Could not load settings: {e}")
        app.config["settings"] = None

    # Register blueprints
    from web.routes.chat import chat_bp
    from web.routes.research import research_bp

    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(research_bp, url_prefix="/api")

    # Health check endpoint
    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    return app


def main():
    """Run the Flask development server."""
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    main()
