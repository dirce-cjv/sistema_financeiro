from __future__ import annotations


def normalize_category_text(raw: str) -> str:
    """Extrai a primeira linha da resposta do modelo, remove aspas comuns e normaliza vazio para 'não identificado'."""
    if not raw:
        return "não identificado"
    line = raw.strip().splitlines()[0].strip()
    line = line.strip('"').strip("'").strip("`").strip()
    return line if line else "não identificado"
