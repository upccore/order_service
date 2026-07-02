import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
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


class OutboxEventModel(Base):
    __tablename__ = "outbox_events"

    id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    event_type = sa.Column(sa.Text, nullable=False)
    payload = sa.Column(JSONB, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    published_at = sa.Column(sa.DateTime(timezone=True), nullable=True)


class InboxEventModel(Base):
    __tablename__ = "inbox_events"

    id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    topic = sa.Column(sa.Text, nullable=False)
    partition = sa.Column(sa.Integer, nullable=False)
    offset = sa.Column(sa.BigInteger, nullable=False)
    processed_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    __table_args__ = (
        sa.UniqueConstraint(
            "topic",
            "partition",
            "offset",
            name="uq_inbox_events_topic_partition_offset",
        ),
    )
