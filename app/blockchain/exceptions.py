class BlockchainError(Exception):
    """Базовое исключение для всех проблем с блокчейном."""
    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)
        self.original_error = original_error

class NodeConnectionError(BlockchainError):
    """Нет соединения с RPC-нодой."""

class ContractCallError(BlockchainError):
    """Ошибка во время вызова view-функции (call)."""

class TransactionError(BlockchainError):
    """Ошибка при отправке транзакции (transact)."""
