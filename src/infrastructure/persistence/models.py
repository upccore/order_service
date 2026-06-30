import uuid

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(sa.Text, nullable=False)
    item_id = sa.Column(sa.Text, nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)
    status = sa.Column(sa.Text, nullable=False)
    idempotency_key = sa.Column(sa.Text, nullable=False, unique=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
