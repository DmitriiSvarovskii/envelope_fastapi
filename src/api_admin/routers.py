from src.api_admin.role.routers import router as router_role
from src.api_admin.user.routers import router as router_user
from src.api_admin.product.routers import router as router_product
from src.api_admin.category.routers import router as router_category
from src.api_admin.unit.routers import router as router_unit


routers = [
    router_category,
    router_product,
    router_unit,
    router_role,
    router_user,
]
