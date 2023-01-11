from django.urls import path
from . views import home, viewdata,newdata, upload_aadhaar, processAadhar

urlpatterns = [
    path("",home, name="home"),
    path("newdata/",newdata, name="newdata"),
    path("upload/adhar/<int:pk>/", upload_aadhaar, name="upload-adhar"),
    path("viewdata/<int:pk>/", viewdata, name="viewdata"),
    path("process/<int:pk>/", processAadhar, name="processAadhar")
    
    # path("upload/aadhaar", upload_aadhaar, name="upload")
]
