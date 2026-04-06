"""
Contratos para geração de texto em streaming (Gemini).

A implementação concreta pode ser adicionada em `gemini_agent` usando
`client.models.generate_content_stream` quando for necessário expor SSE ou chunks.
"""

from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable


@runtime_checkable
class StreamableTextAgent(Protocol):
    """Contrato para agentes que expõem geração de texto em fragmentos (streaming)."""

    def iter_text_chunks(self, prompt: str) -> Iterator[str]:
        """Itera fragmentos de texto conforme o modelo os emite."""
        ...
