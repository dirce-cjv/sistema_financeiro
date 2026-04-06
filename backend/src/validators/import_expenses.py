from __future__ import annotations

from flask import Request
from werkzeug.datastructures import FileStorage

from validators.exceptions import ValidationError


def get_excel_upload_or_error(request: Request) -> FileStorage:
    """Obtém o arquivo do campo `file` ou levanta `ValidationError` se estiver ausente."""
    file = request.files.get("file")
    if file is None or file.filename == "":
        raise ValidationError("Arquivo Excel e obrigatorio.")
    return file
