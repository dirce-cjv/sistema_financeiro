from flask import Blueprint, jsonify, request

from services.categorization_service import run_batch_categorization
from validators import ValidationError, parse_categorize_request

categorize_blueprint = Blueprint("categorize", __name__)


@categorize_blueprint.post("/categorizar")
def categorizar():
    """Endpoint JSON: categoriza linhas da planilha sem categoria (corpo opcional com `limit`)."""
    try:
        parsed = parse_categorize_request(request)
        result = run_batch_categorization(parsed)
        return jsonify(result), 200
    except ValidationError as error:
        return jsonify({"error": error.message}), error.status_code
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Erro interno: {error}"}), 500
