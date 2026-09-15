"""FastAPI application factory / entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routers import redirect, url


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist yet.
    await init_db()
    yield
    # Shutdown: nothing to clean up explicitly; the async engine's
    # connections are released as sessions close.


app = FastAPI(
    title="URL Shortener API",
    description="A minimal, production-style URL shortening service.",
    version="1.0.0",
    lifespan=lifespan,
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(url.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


# Redirect router is included last: it matches any single path segment
# (`/{short_code}`), so registering it before this point would shadow the
# more specific /api/* and /health routes above.
app.include_router(redirect.router)
