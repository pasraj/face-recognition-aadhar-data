from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from . models import UserProfile, AadharImage, AadharData

from PIL import Image
from numpy import array
from pytesseract import image_to_string
from django.conf import settings
from . aadhaar_read_data import adhaar_read
from rest_framework.response import Response



import requests
import io
import ftfy
import json
# image_url = prefix + request.get_host() + STATIC_URL + "images/logo_80.png"
# back_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(user.back)


def read_image(path_f, path_b):

    # front_image = requests.get(path_b)
    # back_image = requests.get(path_f)

    text_f = image_to_string(Image.open(path_f))
    text_b = image_to_string(Image.open(path_b))
    text = text_f + text_b
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    data = adhaar_read(text)
    return data
        
        
def hello(request):
    return render(request,"signup.html")



def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        pan_number = request.POST['pan']
        aadhar_number = request.POST['aadhar']
        password = request.POST['password']

        # create user
        user = User.objects.create(username=email, first_name=name, email=email)
        user.set_password(password)
        user.save()

        # userprofile
        userprofile = UserProfile(name=name,
            user = user,
            dob=dob, 
            adhar_number=aadhar_number,
            pan_number=pan_number,
            phone_number=phone)

        userprofile.save()
    return HttpResponse("Done")


def upload_aadhaar(request):
    if request.method == "GET":
        return render(request, 'aadhar.html')
    if request.method == "POST":
        front_image = request.FILES['front']
        back_image = request.FILES['back']

        data = read_image(front_image, back_image)
        print(data)

        return HttpResponse(json.dumps(data), content_type="application/json")

