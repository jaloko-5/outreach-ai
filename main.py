from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes.health import router as health_router
from app.api.routes.auth_google import router as auth_google_router
from app.api.routes.campaigns import router as campaigns_router
from app.db.base import Base
from app.db.session import engine


settings = get_settings()

app = FastAPI(title="Mystrika-like Email Automation API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"service": settings.app_name, "status": "ok"}


app.include_router(health_router, prefix="/api")
app.include_router(auth_google_router, prefix="/api")
app.include_router(campaigns_router, prefix="/api")