from django.urls import path
from .views import ProductList, create_order

urlpatterns = [
    path('products', ProductList.as_view(), name='products'),
    path('create-order', create_order, name='create-order'),
]