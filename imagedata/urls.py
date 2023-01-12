from django.urls import path
from . views import home, viewdata,newdata, upload_aadhaar, processAadhar, upload_face

urlpatterns = [
    path("",home, name="home"),
    path("newdata/",newdata, name="newdata"),
    path("upload/face/<int:pk>/", upload_face, name="upload_face"),
    path("upload/adhar/<int:pk>/", upload_aadhaar, name="upload-adhar"),
    path("viewdata/<int:pk>/", viewdata, name="viewdata"),
    path("process/<int:pk>/", processAadhar, name="processAadhar")
    
]
