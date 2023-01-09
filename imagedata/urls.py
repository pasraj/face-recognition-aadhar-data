from django.urls import path
from . views import home, viewdata,newdata

urlpatterns = [
    path("",home, name="home"),
    path("newdata/",newdata, name="newdata"),
    path("viewdata/<int:pk>/", viewdata, name="viewdata")
    
    # path("upload/aadhaar", upload_aadhaar, name="upload")
]
