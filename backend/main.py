from __future__ import annotations

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent
_SRC = _BACKEND_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask
from flask_cors import CORS

from config import Config
from routes.categorize_routes import categorize_blueprint
from routes.health_routes import health_blueprint
from routes.import_routes import import_blueprint
from routes.process_routes import process_blueprint


def create_app() -> Flask:
    """Cria a aplicação Flask, aplica CORS e registra os blueprints da API."""
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(health_blueprint)
    app.register_blueprint(import_blueprint)
    app.register_blueprint(categorize_blueprint)
    app.register_blueprint(process_blueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
