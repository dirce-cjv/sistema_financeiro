from __future__ import annotations

from typing import Iterator

from google import genai

from agent.streaming import StreamableTextAgent
from config import Config

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    """Retorna o cliente Gemini singleton, exigindo `GEMINI_API_KEY` configurada."""
    global _client
    if not Config.GEMINI_API_KEY:
        raise ValueError("Defina GEMINI_API_KEY no arquivo .env.")
    if _client is None:
        _client = genai.Client(api_key=Config.GEMINI_API_KEY)
    return _client


class GeminiAgent(StreamableTextAgent):
    """
    Integração com Gemini: recebe o prompt e devolve o texto bruto da API.
    Normalização e regras de negócio ficam nos services.
    """

    def generate_text(self, prompt: str) -> str:
        """Envia o prompt ao modelo configurado e devolve o texto da resposta ou string vazia em falha."""
        client = _get_client()
        try:
            response = client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt,
            )
        except Exception:
            return ""
        return (getattr(response, "text", None) or "").strip()

    def iter_text_chunks(self, prompt: str) -> Iterator[str]:
        """Reservado para streaming; implementar com generate_content_stream quando necessário."""
        raise NotImplementedError(
            "Streaming não implementado. Use generate_text ou estenda com generate_content_stream."
        )
