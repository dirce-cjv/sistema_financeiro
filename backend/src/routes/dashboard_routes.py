from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from services.dashboard_service import build_expenses_by_category

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.get("/dados_dashboard")
def dados_dashboard():
    """Retorna dados agregados de despesas por categoria para o dashboard."""
    try:
        result = build_expenses_by_category()
        return jsonify(result), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Erro interno: {error}"}), 500


@dashboard_blueprint.get("/dashboard")
def dashboard_page():
    """Página HTML do dashboard financeiro (MVP)."""
    return render_template("dashboard.html")
