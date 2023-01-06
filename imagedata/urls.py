from django.urls import path
from . views import hello, signup

urlpatterns = [
    path("",hello, name="Hello"),
    path("signup",signup, name="signup")
]
