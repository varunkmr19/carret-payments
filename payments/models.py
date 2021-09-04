import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  auth_key = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)

class Product(models.Model):
  title = models.CharField(max_length=120)
  description = models.TextField(blank=True, null=True)
  price = models.IntegerField(default=0) # in paisa (1/100th of rupee)

  def __str__(self):
    return self.title

class Transaction(models.Model):
  STATUS = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
  ]
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
  order_id = models.CharField(max_length=500, db_index=True, editable=False, unique=True)
  payment_status = models.CharField(max_length=120, choices=STATUS, default='pending')
  total_amount = models.IntegerField(default=0) # in paisa (1/100th of rupee)
  razorpay_order_id = models.CharField(max_length=120, null=True, blank=True)
  razorpay_payment_id = models.CharField(max_length=120, null=True, blank=True)
  razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.product.title