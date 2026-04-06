from __future__ import annotations

from typing import Any

from flask import Request

from validators.exceptions import ValidationError


def parse_categorize_request(request: Request) -> dict[str, Any]:
    """
    Corpo opcional JSON: { "limit": <int positivo opcional> }.
    Sem corpo: processa todas as linhas sem categoria.
    """
    if request.content_length in (None, 0):
        return {}

    if not request.is_json:
        raise ValidationError("Content-Type deve ser application/json ou envie corpo vazio.")

    data = request.get_json(silent=True)
    if data is None:
        if (request.content_length or 0) > 0:
            raise ValidationError("JSON invalido.")
        return {}

    if not isinstance(data, dict):
        raise ValidationError("O corpo deve ser um objeto JSON.")

    if not data:
        return {}

    unknown = set(data.keys()) - {"limit"}
    if unknown:
        raise ValidationError(
            "Campos nao permitidos: " + ", ".join(sorted(unknown)) + "."
        )

    if "limit" not in data:
        raise ValidationError('Unico campo opcional permitido: "limit".')

    limit = data["limit"]
    if limit is None:
        raise ValidationError('O campo "limit" nao pode ser nulo.')

    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValidationError('O campo "limit" deve ser um numero inteiro positivo.')

    if limit < 1:
        raise ValidationError('O campo "limit" deve ser maior ou igual a 1.')

    return {"limit": limit}
