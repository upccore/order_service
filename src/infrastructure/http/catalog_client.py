from decimal import Decimal

import httpx

from src.application.ports.catalog_client import CatalogClient, CatalogItem
from src.settings import settings


class HttpCatalogClient(CatalogClient):

    async def get_item(self, item_id: str) -> CatalogItem:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.catalog_base_url}/api/catalog/items/{item_id}",
                headers={"X-API-Key": settings.catalog_api_key},
            )
            response.raise_for_status()
            data = response.json()
            return CatalogItem(
                id=data["id"],
                name=data["name"],
                price=Decimal(data["price"]),
                available_qty=data["available_qty"],
            )
