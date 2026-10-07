from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from database import get_session
from models import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create", response_model=Order)
def create_order(order: OrderCreate, session: Annotated[Session, Depends(get_session)]):
    db_order = Order(**order.model_dump())

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order


@router.get("/", response_model=list[Order])
def get_orders(
    session: Annotated[Session, Depends(get_session)],
    status: Annotated[
        OrderStatus | None,
        Query(description="Filter orders by status"),
    ] = None,
    created_date: Annotated[
        str | None,
        Query(description="Filter orders by creation date (YYYY-MM-DD)"),
    ] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        parsed_date = date.fromisoformat(created_date)
        start = datetime.combine(parsed_date, datetime.min.time())
        end = datetime.combine(parsed_date, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    orders = session.exec(query).all()

    return orders


@router.get("/{order_id}")
def get_order(order_id: int, session: Annotated[Session, Depends(get_session)]):
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.patch("/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_update.status:
        order.status = order_update.status

    if order_update.delivery_address:
        order.delivery_address = order_update.delivery_address

    order.updated_at = datetime.now(UTC)

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, session: Annotated[Session, Depends(get_session)]):
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    session.delete(order)
    session.commit()

    return {"message": "Order deleted successfully"}
