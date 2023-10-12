from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.category.routers import router as router_category
from src.product.routers import router as router_product
from src.cart.routers import router as router_cart
from src.order.routers import router as router_order
from src.customer.routers import router as router_customer
from src.user.routers import router as router_user
from src.employee.routers import router as router_employee
from src.auth.routers import router as router_auth


app = FastAPI(
    title="Garage cafe",
    version="1.0.0a",
)

app.openapi_schema = None


app.mount("/media", StaticFiles(directory="media"), name="media")


app.include_router(router_auth)
app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_cart)
app.include_router(router_order)
app.include_router(router_customer)
app.include_router(router_user)
app.include_router(router_employee)


origins = [
    "http://localhost:8000",
    "https://swarovskidmitrii.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
