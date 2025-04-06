from math import ceil
import redis.asyncio as redis

from contextlib import asynccontextmanager
from decouple import config
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Response,
)
from fastapi_limiter import FastAPILimiter

REDIS_URL = config("REDIS_URL")


async def rate_limit_exceeded_handler(
    request: Request, response: Response, pexpire: int
):
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        status_code=429,
        detail="Too Many Requests, try again soon.",
        headers={"Retry-After": str(expire)},
    )


async def rate_limit_identifier(request: Request):
    # return f"user:1:{request.scope["path"]}"
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host + ":" + request.scope["path"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_conn = redis.from_url(REDIS_URL)
    await FastAPILimiter.init(
        redis_conn,
        identifier=rate_limit_identifier,
        http_callback=rate_limit_exceeded_handler,
    )
    yield
    await FastAPILimiter.close()
