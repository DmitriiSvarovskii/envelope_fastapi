from .role import Role
from .user import User
from .category import Category
from .subcategory import Subcategory
from .product import Unit, Product
from .employee import Employee
from .auth import Token
from .cart import Cart
from .order import Order, OrderDetail, OrderCustomerInfo
from .mail import Mail, MailImage
from .customer import Customer
from .payment import PaymentYookassa
from .store import (
    Store,
    BotToken,
    OrderType,
    StoreOrderTypeAssociation,
    StoreInfo,
    StoreSubscription,
    DayOfWeek,
    WorkingDay,
    StorePayment,
    ServiceTextAndChat,
    LegalInformation,

    DeliveryDistance,
    DeliveryFix,
    DeliveryDistrict,
    TypeDelivery
)


all = (
    'Employee',
    'Role',
    'User',
    'Catyegory',
    'Subcategory',
    'Unit',
    'Product',
    'Token',
    'Cart',
    'Order',
    'OrderDetail',
    'OrderCustomerInfo',
    'Customer',
    'Mail',
    'MailImage',
    'Store',
    'BotToken',
    'OrderType',
    'StoreOrderTypeAssociation',
    'StoreInfo',
    'StoreSubscription',
    'DayOfWeek',
    'WorkingDay',
    'StorePayment',
    'ServiceTextAndChat',
    'LegalInformation',

    'DeliveryDistance',
    'DeliveryFix',
    'DeliveryDistrict',
    'TypeDelivery',
    'PaymentYookassa',
)

model_for_public = [
    Role,
    User,
    Unit,
    Token,
    BotToken,
    OrderType,
    DayOfWeek,
    Employee,
    TypeDelivery,

]


model_for_new_schema = [
    Store.__table__,
    Category.__table__,
    Subcategory.__table__,
    Product.__table__,
    Customer.__table__,
    Cart.__table__,
    MailImage.__table__,
    Mail.__table__,
    Order.__table__,
    OrderDetail.__table__,
    OrderCustomerInfo.__table__,
    StoreOrderTypeAssociation.__table__,
    StoreInfo.__table__,
    StoreSubscription.__table__,
    WorkingDay.__table__,
    StorePayment.__table__,
    ServiceTextAndChat.__table__,
    LegalInformation.__table__,
    DeliveryDistance.__table__,
    DeliveryFix.__table__,
    DeliveryDistrict.__table__,
    PaymentYookassa.__table__,
]
