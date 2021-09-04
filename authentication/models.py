import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  auth_key = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
  phone_number = models.CharField(max_length=10, null=True, blank=True)

