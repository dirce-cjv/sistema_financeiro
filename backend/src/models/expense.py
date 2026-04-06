from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


class ExpenseRowDict(TypedDict):
    """Linha de despesa após leitura do Excel (chaves alinhadas ao legado)."""

    Data: str
    Descricao: str
    Valor: str


@dataclass(frozen=True)
class ExpenseRow:
    """Uma linha de despesa normalizada após importação (data, descrição e valor como string)."""

    data: str
    descricao: str
    valor: str

    def to_sheet_row_cells(self, expense_id: str) -> list[str]:
        """Monta as células da linha na planilha: ID, data, descrição, valor e categoria vazia."""
        return [expense_id, self.data, self.descricao, self.valor, ""]

    @classmethod
    def from_dict(cls, row: ExpenseRowDict) -> ExpenseRow:
        """Instancia `ExpenseRow` a partir do dicionário tipado `ExpenseRowDict`."""
        return cls(
            data=row["Data"],
            descricao=row["Descricao"],
            valor=row["Valor"],
        )


@dataclass(frozen=True)
class PendingSheetRow:
    """Linha da planilha aguardando categoria."""

    row: int
    expense_id: str
    description: str
