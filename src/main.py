from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_admin.routers import routers


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)


ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
    "https://swarovskidmitrii.ru",
    "https://www.swarovskidmitrii.ru",
]


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


for router in routers:
    app.include_router(router)
