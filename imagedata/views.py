from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from . models import UserProfile, AadharImage, AadharData

from PIL import Image
from numpy import array
from pytesseract import image_to_string
from django.conf import settings
from . aadhaar_read_data import adhaar_read



import requests
import io
import ftfy
# image_url = prefix + request.get_host() + STATIC_URL + "images/logo_80.png"
# back_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(user.back)


def read_image(path_f, path_b):

    front_image = requests.get(path_b)
    back_image = requests.get(path_f)
    text_f = image_to_string(Image.open(io.BytesIO(front_image.content)), lang = 'eng')
    text_b = image_to_string(Image.open(io.BytesIO(back_image.content)), lang = 'eng')
    text = text_f + text_b
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    data = adhaar_read(text)
    return data
        
        
def hello(request):
    return HttpResponse("Hello, World!")


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