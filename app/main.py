from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import auth, users, chat, admin
from app.db import models
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Creating database tables...")
    # open a real connection/transaction context for DDL
    with engine.begin() as conn:
        models.Base.metadata.create_all(bind=conn)
    print("Database tables created successfully.")
    yield
    print("Application shutdown.")

app = FastAPI(title="Tenhance AI Chat Backend", lifespan=lifespan)

app.include_router(auth.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
app.include_router(chat.router, prefix="/v1")
app.include_router(admin.router, prefix="/v1", tags=["Admin"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}