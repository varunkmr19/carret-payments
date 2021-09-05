from django.urls import path
from .views import ProductList, create_order, verify_payment

urlpatterns = [
    path('products', ProductList.as_view(), name='products'),
    path('create-order', create_order, name='create-order'),
    path('verify-payment', verify_payment, name='verify-payment')
]