from src.api_admin.user.routers import router as router_user
from src.api_admin.role.routers import router as router_role
from src.api_admin.product.routers import router as router_product
from src.api_admin.product.routers_unit import router as router_unit
from src.api_admin.category.routers import router as router_category
from src.api_admin.subcategory.routers import router as router_subcategory
from src.api_admin.auth.routers import router as router_auth
from src.api_admin.store.routers import router as router_store
from src.api_admin.cart.routers import router as router_cart
from src.api_admin.customer.routers import router as router_customer
from src.api_admin.order.routers import router as router_order


routers = [
    router_auth,
    router_category,
    router_subcategory,
    router_product,
    router_unit,
    router_user,
    router_role,
    router_store,
    router_order,
    router_customer,
    router_cart,
]
