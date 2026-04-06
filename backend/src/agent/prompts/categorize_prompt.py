from __future__ import annotations


def build_categorize_prompt(description: str) -> str:
    """Retorna apenas o texto do prompt enviado ao modelo (sem lógica de negócio)."""

    return f"""Classifique a despesa a partir da descrição abaixo.

Regras:
- Responda com UMA única linha contendo somente o nome da categoria.
- Use categorias claras e objetivas (ex.: Alimentação, Transporte, Moradia, Lazer, Saúde, Assinaturas, Receita).
- Se a descrição for insuficiente ou ambígua, responda exatamente: não identificado
- Não inclua aspas, markdown, numeração ou texto explicativo.

Descrição:
{description}
"""
