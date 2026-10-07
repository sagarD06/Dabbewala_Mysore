from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, func, select

from database import get_session
from models import Order, OrderStatus

router = APIRouter(prefix="/order_summary", tags=["Order_Summary"])


@router.get("/", response_model=dict)
def get_order_summary(
    session: Annotated[Session, Depends(get_session)],
    summary_date: Annotated[
        date | None, Query(description="Date for summary in (YYYY-MM-DD)")
    ] = None,
):
    if summary_date is None:
        summary_date = datetime.now(UTC).today()

    start = datetime.combine(summary_date, datetime.min.time(), tzinfo=UTC)
    end = datetime.combine(summary_date, datetime.max.time(), tzinfo=UTC)

    summary = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(  # type: ignore
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == status,
            )
        ).one()
        summary[status.value] = count
        total += count

    return {
        "date": summary_date.isoformat(),
        "total_orders": total,
        "orders_by_status": summary,
    }
