from decimal import Decimal
from urllib.parse import urljoin

import httpx

from src.application.ports.catalog_client import (
    CatalogClient,
    CatalogItem,
    CatalogServiceError,
)
from src.settings import settings


class HttpCatalogClient(CatalogClient):

    async def get_item(self, item_id: str) -> CatalogItem:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    urljoin(settings.catalog_base_url, f"/api/catalog/items/{item_id}"),
                    headers={"X-API-Key": settings.catalog_api_key},
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as e:
            raise CatalogServiceError(str(e)) from e

        return CatalogItem(
            id=data["id"],
            name=data["name"],
            price=Decimal(data["price"]),
            available_qty=data["available_qty"],
        )
