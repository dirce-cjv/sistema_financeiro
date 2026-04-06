from __future__ import annotations

from werkzeug.datastructures import FileStorage

from integrations.excel_reader import read_expenses_excel
from integrations.google_sheets import GoogleSheetsClient


def import_expenses_from_upload(file_storage: FileStorage) -> dict[str, int | str | None]:
    """
    Fluxo: leitura Excel → montagem de linhas → append na planilha.
    """
    expenses = read_expenses_excel(file_storage)
    sheets = GoogleSheetsClient()

    last_id = sheets.get_last_id()
    rows_to_insert: list[list[str]] = []

    for index, expense in enumerate(expenses, start=1):
        rows_to_insert.append(expense.to_sheet_row_cells(str(last_id + index)))

    sheets.append_rows(rows_to_insert)

    return {
        "message": "Importacao concluida com sucesso.",
        "imported_rows": len(rows_to_insert),
        "start_id": last_id + 1 if rows_to_insert else None,
        "end_id": last_id + len(rows_to_insert) if rows_to_insert else None,
    }
