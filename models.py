from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name : str
    delivery_address: str
    items: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class OrderCreate(SQLModel):
    customer_name: str
    delivery_address: str
    items: str

class OrderUpdate(SQLModel):
    status: OrderStatus | None = None
    delivery_address: str | None = None

class StatusLog(SQLModel):
    order_id: int
    old_status: OrderStatus
    new_status: OrderStatus
    updated_at: datetime