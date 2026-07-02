from src.application.usecases.create_order import CreateOrderUseCase
from src.application.usecases.get_order import GetOrderUseCase
from src.application.usecases.process_payment_callback import (
    ProcessPaymentCallbackUseCase,
)
from src.infrastructure.http.catalog_client import HttpCatalogClient
from src.infrastructure.http.notifications_client import HttpNotificationsClient
from src.infrastructure.http.payments_client import HttpPaymentsClient
from src.infrastructure.persistence.database import session_factory
from src.infrastructure.persistence.uow import UnitOfWork


def get_create_order_use_case() -> CreateOrderUseCase:
    uow = UnitOfWork(session_factory)
    catalog = HttpCatalogClient()
    payments = HttpPaymentsClient()
    notifications = HttpNotificationsClient()
    return CreateOrderUseCase(
        uow=uow, catalog=catalog, payments=payments, notifications=notifications
    )


def get_get_order_use_case() -> GetOrderUseCase:
    uow = UnitOfWork(session_factory)
    return GetOrderUseCase(uow=uow)


def get_process_payment_callback_use_case() -> ProcessPaymentCallbackUseCase:
    uow = UnitOfWork(session_factory)
    notifications = HttpNotificationsClient()
    return ProcessPaymentCallbackUseCase(uow=uow, notifications=notifications)
