from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    name = models.CharField(max_length=100, null=True)
    dob = models.DateField(max_length=20, null=True)
    aadhaar_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=300, null=True, default=None)
    pincode = models.CharField(max_length=10, null=True, default=None)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=10, null=True) # MALE FEMALE enum
    pic = models.FileField(upload_to='profile', default=None, null=True)

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
    is_name_matched = models.BooleanField(default=False, null=True)
    dob = models.CharField(max_length=20, null=True)
    is_dob_matched = models.BooleanField(default=False, null=True)
    sex = models.CharField(max_length=10, null=True)
    is_sex_matched = models.BooleanField(default=False, null=True)
    aadhaar_number = models.CharField(max_length=20, null=True)
    is_adhar_matched = models.BooleanField(default=False, null=True)
    address = models.CharField(max_length=400, null=True)
    pincode = models.CharField(max_length=10, null=True)
    is_pincode_matched = models.BooleanField(default=False, null=True)
    netcopy = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.profile.name

