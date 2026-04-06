from datetime import date, datetime

import pandas as pd

from models.expense import ExpenseRow, ExpenseRowDict

EXPECTED_COLUMNS = ["Data", "Descricao", "Valor"]
ALTERNATIVE_COLUMNS = ["Data", "Descrição", "Valor"]


def _to_serializable_date(value) -> str:
    """Converte células de data (Timestamp, datetime, date ou texto) para `YYYY-MM-DD` ou string vazia."""
    if pd.isna(value):
        return ""

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")

    return str(value).strip()


def read_expenses_excel(file_storage) -> list[ExpenseRow]:
    """Lê um Excel com colunas Data, Descrição e Valor e devolve uma lista de `ExpenseRow`."""
    dataframe = pd.read_excel(file_storage)

    columns = list(dataframe.columns)
    if columns == ALTERNATIVE_COLUMNS:
        dataframe.columns = EXPECTED_COLUMNS
        columns = EXPECTED_COLUMNS

    if columns != EXPECTED_COLUMNS:
        raise ValueError("O Excel deve conter exatamente as colunas: Data, Descrição, Valor.")

    dataframe = dataframe.dropna(how="all")
    if dataframe.empty:
        raise ValueError("O arquivo Excel nao possui linhas para importacao.")

    expenses: list[ExpenseRow] = []
    for _, row in dataframe.iterrows():
        raw: ExpenseRowDict = {
            "Data": _to_serializable_date(row["Data"]),
            "Descricao": str(row["Descricao"]).strip() if not pd.isna(row["Descricao"]) else "",
            "Valor": "" if pd.isna(row["Valor"]) else str(row["Valor"]).strip(),
        }
        expenses.append(ExpenseRow.from_dict(raw))

    return expenses
