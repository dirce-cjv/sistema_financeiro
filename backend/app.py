"""Ponto de entrada legado; prefira `python main.py`."""

from main import app, create_app

__all__ = ["app", "create_app"]

if __name__ == "__main__":
    from config import Config

    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
