from src.api_admin.user.routers import router as router_user
from src.api_admin.product.routers import router as router_product
from src.api_admin.category.routers import router as router_category


routers = [
    router_category,
    router_product,
    router_user,
]
