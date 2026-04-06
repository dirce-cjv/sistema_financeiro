class ValidationError(Exception):
    """Erro de validação de entrada da API."""

    def __init__(self, message: str, status_code: int = 400):
        """Armazena a mensagem amigável e o código HTTP associado ao erro de validação."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
