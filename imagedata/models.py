from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=20, null=True)
    adhar_number = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=400, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"name : {self.name}"
