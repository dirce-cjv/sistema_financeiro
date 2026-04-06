from __future__ import annotations

from typing import Any

from flask import Request
from werkzeug.datastructures import FileStorage

from validators.exceptions import ValidationError


def parse_process_request(request: Request) -> dict[str, Any]:
    """
    POST /processar:
    - multipart com campo `file`: importação Excel.
    - JSON com \"acao\": \"categorizar\": mesmas regras de corpo que /categorizar.
    """
    if request.files.get("file") and request.files.get("file").filename:
        return {"tipo": "importar", "file": request.files.get("file")}

    if request.content_length in (None, 0):
        raise ValidationError('Envie um arquivo (campo \"file\") ou JSON com \"acao\": \"categorizar\".')

    if not request.is_json:
        raise ValidationError("Para categorizar, use Content-Type application/json.")

    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("JSON invalido.")

    if not isinstance(data, dict):
        raise ValidationError("O corpo deve ser um objeto JSON.")

    acao = data.get("acao")
    if acao != "categorizar":
        raise ValidationError('Para categorizar, informe \"acao\": \"categorizar\".')

    unknown = set(data.keys()) - {"acao", "limit"}
    if unknown:
        raise ValidationError(
            "Campos nao permitidos: " + ", ".join(sorted(unknown)) + "."
        )

    if "limit" not in data:
        return {"tipo": "categorizar", "options": {}}

    limit = data["limit"]
    if limit is None:
        raise ValidationError('O campo "limit" nao pode ser nulo.')
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValidationError('O campo "limit" deve ser um numero inteiro positivo.')
    if limit < 1:
        raise ValidationError('O campo "limit" deve ser maior ou igual a 1.')

    return {"tipo": "categorizar", "options": {"limit": limit}}
