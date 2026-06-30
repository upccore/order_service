from fastapi import FastAPI
from src.presentation.api.routes.orders import router as orders_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(orders_router)
    return app
