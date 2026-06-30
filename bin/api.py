import uvicorn
from alembic import command
from alembic.config import Config

from src.fastapi import create_app


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


app = create_app()

if __name__ == "__main__":
    run_migrations()
    uvicorn.run(app, host="0.0.0.0", port=8000)
