from __future__ import annotations

from integrations.google_sheets import GoogleSheetsClient

DEFAULT_CATEGORIES = ["Alimentação", "Transporte", "Moradia", "Lazer", "Outros"]


def _parse_brl_number(raw: str) -> float | None:
    """
    Converte valores da planilha para float.
    Suporta formatos como: -123.45, -123,45, R$ -1.234,56.
    """
    text = (raw or "").strip()
    if not text:
        return None

    sanitized = text.replace("R$", "").replace(" ", "")

    if "," in sanitized and "." in sanitized:
        # Caso comum no Brasil: 1.234,56 -> 1234.56
        sanitized = sanitized.replace(".", "").replace(",", ".")
    elif "," in sanitized:
        sanitized = sanitized.replace(",", ".")

    try:
        return float(sanitized)
    except ValueError:
        return None


def build_expenses_by_category() -> dict[str, dict[str, float]]:
    """
    Lê linhas da planilha, filtra apenas despesas (valores negativos),
    agrupa por categoria e soma os valores absolutos.
    """
    sheets = GoogleSheetsClient()
    rows = sheets.get_expense_rows_for_dashboard()

    totals: dict[str, float] = {category: 0.0 for category in DEFAULT_CATEGORIES}

    for row in rows:
        value = _parse_brl_number(row.get("valor", ""))
        if value is None or value >= 0:
            continue

        category = (row.get("categoria", "") or "").strip()
        if not category:
            category = "Outros"

        if category not in totals:
            totals["Outros"] += abs(value)
            continue

        totals[category] += abs(value)

    return {"despesas_por_categoria": totals}
