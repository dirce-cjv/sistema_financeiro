from __future__ import annotations

from flask import Blueprint, jsonify

health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/teste")
def health_check():
    """Responde com status simples para verificar se o servidor está ativo."""
    return jsonify({"message": "Servidor financeiro ativo"}), 200
