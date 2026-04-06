from __future__ import annotations

import gspread
from gspread import Worksheet

from config import Config
from models.expense import PendingSheetRow

# Colunas: A=ID, B=Data, C=Descrição, D=Valor, E=Categoria (1-based)
COL_ID = 1
COL_DESCRIPTION = 3
COL_CATEGORY = 5


class GoogleSheetsClient:
    """Acesso à planilha: leitura/escrita sem regras de negócio."""

    def __init__(self) -> None:
        """Abre a planilha e a aba definidas em `Config` usando a conta de serviço."""
        if not Config.GOOGLE_SHEETS_ID:
            raise ValueError("Defina GOOGLE_SHEETS_ID no arquivo .env.")

        if not Config.GOOGLE_SERVICE_ACCOUNT_FILE:
            raise ValueError("Defina GOOGLE_SERVICE_ACCOUNT_FILE no arquivo .env.")

        client = gspread.service_account(filename=Config.GOOGLE_SERVICE_ACCOUNT_FILE)
        spreadsheet = client.open_by_key(Config.GOOGLE_SHEETS_ID)
        self.worksheet: Worksheet = spreadsheet.worksheet(Config.GOOGLE_SHEETS_WORKSHEET)

    def get_last_id(self) -> int:
        """Maior ID numérico na coluna A (exceto cabeçalho); 0 se não houver IDs válidos."""
        values = self.worksheet.col_values(COL_ID)
        if len(values) <= 1:
            return 0

        max_id = 0
        for value in values[1:]:
            try:
                max_id = max(max_id, int(value))
            except ValueError:
                continue
        return max_id

    def append_rows(self, rows: list[list[str]]) -> None:
        """Anexa linhas ao final da planilha com entrada como usuário (`USER_ENTERED`)."""
        if not rows:
            return
        self.worksheet.append_rows(rows, value_input_option="USER_ENTERED")

    def get_rows_without_category(self, limit: int | None = None) -> list[PendingSheetRow]:
        """Lista linhas (a partir da 2) com coluna de categoria vazia; opcionalmente corta em `limit` itens."""
        all_values = self.worksheet.get_all_values()
        if len(all_values) <= 1:
            return []

        result: list[PendingSheetRow] = []
        for row_index, row in enumerate(all_values[1:], start=2):
            padded = (row + [""] * COL_CATEGORY)[:COL_CATEGORY]
            category_cell = str(padded[COL_CATEGORY - 1]).strip()
            if category_cell:
                continue

            description = str(padded[COL_DESCRIPTION - 1]).strip() if padded[COL_DESCRIPTION - 1] else ""
            expense_id = str(padded[COL_ID - 1]).strip() if padded[COL_ID - 1] else ""

            result.append(
                PendingSheetRow(
                    row=row_index,
                    expense_id=expense_id,
                    description=description,
                )
            )

            if limit is not None and len(result) >= limit:
                break

        return result

    def update_category_cells(self, row_category_pairs: list[tuple[int, str]]) -> None:
        """Atualiza em lote a coluna E (categoria) para cada par (número da linha, texto da categoria)."""
        if not row_category_pairs:
            return

        batch_payload = [
            {"range": f"E{row}", "values": [[category]]}
            for row, category in row_category_pairs
        ]
        self.worksheet.batch_update(batch_payload, value_input_option="USER_ENTERED")
