from src.application.usecases.create_order import CreateOrderUseCase
from src.application.usecases.get_order import GetOrderUseCase
from src.infrastructure.http.catalog_client import HttpCatalogClient
from src.infrastructure.http.payments_client import HttpPaymentsClient
from src.infrastructure.persistence.database import session_factory
from src.infrastructure.persistence.uow import UnitOfWork


def get_create_order_use_case() -> CreateOrderUseCase:
    uow = UnitOfWork(session_factory)
    catalog = HttpCatalogClient()
    payments = HttpPaymentsClient()
    return CreateOrderUseCase(uow=uow, catalog=catalog, payments=payments)


def get_get_order_use_case() -> GetOrderUseCase:
    uow = UnitOfWork(session_factory)
    return GetOrderUseCase(uow=uow)
