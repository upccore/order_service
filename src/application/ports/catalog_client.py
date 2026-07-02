from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CatalogItem:
    id: str
    name: str
    price: Decimal
    available_qty: int


class CatalogServiceError(Exception):
    """Не удалось получить товар из Catalog Service"""


class CatalogClient(ABC):

    @abstractmethod
    async def get_item(self, item_id: str) -> CatalogItem: ...
