from flask import Blueprint, jsonify, request

from services.import_service import import_expenses_from_upload
from validators import ValidationError, get_excel_upload_or_error

import_blueprint = Blueprint("import", __name__, url_prefix="/import")


@import_blueprint.post("/expenses")
def import_expenses():
    """Recebe upload multipart com campo `file` (Excel) e grava as despesas na planilha."""
    try:
        file = get_excel_upload_or_error(request)
        result = import_expenses_from_upload(file)
        return jsonify(result), 200
    except ValidationError as error:
        return jsonify({"error": error.message}), error.status_code
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Erro interno: {error}"}), 500
