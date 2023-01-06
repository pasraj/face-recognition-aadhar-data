from django.contrib import admin
from . models import UserProfile, AadharImage, AadharData

# Register your models here.

admin.site.register([UserProfile, AadharImage, AadharData])
