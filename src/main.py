from fastapi_users import FastAPIUsers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api_admin.routers import routers
# from src.config import ORIGINS
# from fastapi_users import fastapi_users

# # from src.api_admin.auth.models import User
# from src.api_admin.auth.manager import get_user_manager
# from src.api_admin.auth.auth import auth_backend
# from src.api_admin.auth.schemas import UserCreate, UserRead, UserUpdate


app = FastAPI(
    title="Envelope-app",
    version="1.0.0a",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url=None,
)

# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

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

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/api/v1/auth/jwt",
#     tags=["Auth"],
# )

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/api/v1/auth",
#     tags=["Auth"],
# )

# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/api/v1/auth",
#     tags=["Auth"],
# )


for router in routers:
    app.include_router(router)
