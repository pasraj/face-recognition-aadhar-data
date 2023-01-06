from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=20, null=True)
    adhar_number = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def email(self):
        return f"{self.user.email}"


class AadharImage(models.Model):
    front_image = models.FileField(upload_to='front')
    back_image = models.FileField(upload_to='back')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.name


class AadharData(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=20, null=True)
    adhar_number = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=400, null=True)

    def __str__(self) -> str:
        return self.profile.name

