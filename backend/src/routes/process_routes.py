from flask import Blueprint, jsonify, request

from services.categorization_service import run_batch_categorization
from services.import_service import import_expenses_from_upload
from validators.exceptions import ValidationError
from validators.process import parse_process_request

process_blueprint = Blueprint("process", __name__)


@process_blueprint.post("/processar")
def processar():
    """
    POST principal: multipart + `file` → importação; JSON `{\"acao\":\"categorizar\"}` → categorização.
    """
    try:
        spec = parse_process_request(request)
        if spec["tipo"] == "importar":
            result = import_expenses_from_upload(spec["file"])
        else:
            result = run_batch_categorization(spec["options"])
        return jsonify(result), 200
    except ValidationError as error:
        return jsonify({"error": error.message}), error.status_code
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Erro interno: {error}"}), 500
