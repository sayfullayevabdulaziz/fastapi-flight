import time

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.deps import get_redis_client
from app.core.config import settings
from app.api.v1.api import api_router as api_router_v1
from app.db.session import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_redis_client()
    sessionmanager.init(settings.ASYNC_DATABASE_URI)
    print("startup fastapi")
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
    engine_args={
        "echo": False,
    },
)

@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    return {"message": "Hello World"}


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
