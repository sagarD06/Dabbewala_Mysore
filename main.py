from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables
from routes.orders import router as order_router
from routes.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created")
    # clean ups
    yield
    print("shutting down")


app = FastAPI(
    title="Dabbewal App API's",
    description="Creating API for Dabbewala service in Mysore",
    lifespan=lifespan,
)

app.include_router(order_router)
app.include_router(stats_router)


@app.get("/")
def root():
    return {"message": "Welcome to Dabbewala - Mysore"}
