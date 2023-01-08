from django.urls import path
from . views import hello, signup, upload_aadhaar

urlpatterns = [
    path("",hello, name="Hello"),
    path("signup",signup, name="signup"),
    path("upload/aadhaar", upload_aadhaar, name="upload")
]
