from django.contrib import admin
from .models import Product, Transaction, User

# Register your models here.
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(User)
