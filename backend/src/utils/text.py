from __future__ import annotations

import re
import unicodedata

ALLOWED_CATEGORIES = {
    "alimentacao": "Alimentação",
    "transporte": "Transporte",
    "moradia": "Moradia",
    "saude": "Saúde",
    "lazer": "Lazer",
    "assinaturas": "Assinaturas",
    "outros": "Outros",
}

KEYWORDS_BY_CATEGORY = {
    "Alimentação": [
        "supermercado",
        "restaurante",
        "restaurantes",
        "lanche",
        "lanches",
        "almoco",
        "jantar",
        "pastel",
        "pizza",
        "kalzone",
        "comida",
    ],
    "Transporte": [
        "combustivel",
        "gasolina",
        "uber",
        "onibus",
        "transporte",
        "pedagio",
        "pedagios",
        "estacionamento",
        "carro",
        "manutencao",
    ],
    "Moradia": ["aluguel", "energia", "agua", "internet", "telefone", "condominio"],
    "Saúde": ["plano de saude", "consulta", "medico", "medica", "exame", "remedio", "farmacia", "academ"],
    "Lazer": ["cinema", "viagem", "viagens", "passeio", "passeios", "festa", "show"],
    "Assinaturas": ["netflix", "spotify", "amazon", "prime", "youtube premium", "assinatura"],
}


def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_for_matching(raw: str) -> str:
    """Normaliza texto para matching de categorias/palavras-chave."""
    if not raw:
        return ""
    text = unicodedata.normalize("NFKC", str(raw))
    text = text.lower()
    text = _strip_accents(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_description_for_ai(raw: str) -> str:
    """
    Pré-processa descrição antes da IA para reduzir ruído textual:
    - normaliza unicode (NFKC)
    - remove espaços duplicados e quebras de linha
    - aplica lowercase para reduzir variações de maiúsculas/minúsculas
    """
    if not raw:
        return ""

    return normalize_for_matching(raw)


def infer_category_by_keywords(normalized_description: str) -> str | None:
    """Retorna categoria por regra simples de palavras-chave, ou None se não encontrar."""
    text = normalized_description or ""
    if not text:
        return None

    for category, keywords in KEYWORDS_BY_CATEGORY.items():
        if any(keyword in text for keyword in keywords):
            return category
    return None


def canonicalize_category(raw: str) -> str:
    """
    Converte variações de saída da IA para categorias canônicas.
    Saída desconhecida vira 'Outros' para evitar 'não identificado' em massa.
    """
    normalized = normalize_for_matching(raw)
    if not normalized:
        return "Outros"

    # Aceita "saude", "alimentacao", etc.
    if normalized in ALLOWED_CATEGORIES:
        return ALLOWED_CATEGORIES[normalized]

    # Aceita frases como "categoria: transporte"
    for key, canonical in ALLOWED_CATEGORIES.items():
        if key in normalized:
            return canonical

    return "Outros"


def normalize_category_text(raw: str) -> str:
    """Extrai a primeira linha da resposta do modelo, remove aspas comuns e normaliza vazio para 'não identificado'."""
    if not raw:
        return "não identificado"
    line = raw.strip().splitlines()[0].strip()
    line = line.strip('"').strip("'").strip("`").strip()
    return line if line else "não identificado"
