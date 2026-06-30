class OrderNotFoundError(Exception):
    """Заказ не найден"""


class InsufficientStockError(Exception):
    """Недостаточно товара на складе"""


class DuplicateOrderError(Exception):
    """Заказ с таким idempotency_key уже существует"""
