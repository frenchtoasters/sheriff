from fastapi import FastAPI
from contextlib import asynccontextmanager
from sheriff.core.db import init_db
from sheriff.api import routes_recipients, routes_webhook

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes_recipients.router)
app.include_router(routes_webhook.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
