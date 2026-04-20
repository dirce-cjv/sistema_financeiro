from __future__ import annotations

from typing import Any

from agent.gemini_agent import GeminiAgent
from agent.prompts.categorize_prompt import build_categorize_prompt
from integrations.google_sheets import GoogleSheetsClient
from utils.text import (
    canonicalize_category,
    infer_category_by_keywords,
    normalize_category_text,
    normalize_description_for_ai,
)


def run_batch_categorization(options: dict[str, Any]) -> dict[str, Any]:
    """
    Fluxo: planilha → linhas sem categoria → IA → normalização → atualização na planilha.
    options: { "limit": int opcional }
    """
    limit = options.get("limit")

    sheets = GoogleSheetsClient()
    pending = sheets.get_rows_without_category(limit=limit)

    if not pending:
        return {
            "message": "Nenhuma linha sem categoria encontrada.",
            "processed": 0,
            "rows": [],
        }

    agent = GeminiAgent()
    updates: list[tuple[int, str]] = []
    details: list[dict[str, Any]] = []

    for item in pending:
        try:
            text = normalize_description_for_ai(item.description)
            if not text:
                category = "Outros"
            else:
                # 1) Regra local (rápida e barata). 2) IA apenas se necessário.
                rule_based = infer_category_by_keywords(text)
                if rule_based:
                    category = rule_based
                else:
                    raw = agent.generate_text(build_categorize_prompt(text))
                    category = canonicalize_category(normalize_category_text(raw))
        except Exception:
            category = "Outros"

        if not category or not str(category).strip():
            category = "Outros"

        updates.append((item.row, category))
        details.append(
            {
                "row": item.row,
                "id": item.expense_id,
                "categoria": category,
            }
        )

    sheets.update_category_cells(updates)

    return {
        "message": "Categorizacao concluida.",
        "processed": len(details),
        "rows": details,
    }
