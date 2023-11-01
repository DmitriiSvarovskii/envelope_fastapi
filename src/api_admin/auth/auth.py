# from fastapi_users.authentication import JWTStrategy
# from fastapi_users.authentication import CookieTransport
# # from src.config import SECRET_KEY_JWT
# from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy


# cookie_transport = CookieTransport(
#     cookie_max_age=3600, cookie_name='envelope_app')


# SECRET_KEY_JWT = "SECRET_KEY_JWT"


# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET_KEY_JWT, lifetime_seconds=3600)


# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=cookie_transport,
#     get_strategy=get_jwt_strategy,
# )
