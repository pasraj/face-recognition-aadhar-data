from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from . models import UserProfile, AadharImage, AadharData

from PIL import Image
from numpy import array
from pytesseract import image_to_string
from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import redirect

from . aadhaar_read_data import adhaar_read
from .adhardata import data_from_qr



import requests
import io
import ftfy
import json
# image_url = prefix + request.get_host() + STATIC_URL + "images/logo_80.png"
# back_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(user.back)


def read_image(path_f, path_b):

    # front_image = requests.get(path_b)
    # back_image = requests.get(path_f)

    image_f = Image.open(path_f)
    image_b = Image.open(path_b)

    print(type(image_f))

    text_f = image_to_string(image_f)
    text_b = image_to_string(image_b)
    text = text_f + text_b
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    data = adhaar_read(text)
    return data


def home(request):
    return render(request, "enternumber.html")

def viewdata(request, pk):
    try:
        if request.method == "POST":
            user = UserProfile.objects.get(phone_number=request.POST["phone"])
            render(request, "viewdata.html", {"userdata":user})
            
        if request.method == "GET":
            user = UserProfile.objects.get(id=pk)
        return render(request, "viewdata.html", {"userdata":user})
    except:
        return render(request, "viewdata.html")


def newdata(request):
    if request.method == "GET":
        return render(request,"userdata.html")

    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        dob = request.POST['dob']
        aadhar_number = request.POST['aadhaar']

        # userprofile
        userprofile = UserProfile(name=name,
            dob=dob,
            adhar_number=aadhar_number,
            phone_number=phone)
        userprofile.save()
        print("saved data ###########")
        print(userprofile.id)
        url = f"/viewdata/{userprofile.id}"
        return redirect(url)



def upload_aadhaar(request, pk):
    if request.method == "GET":
        user = UserProfile.objects.get(id=pk)
        return render(request, 'aadhar.html', {"userdata":user})
    if request.method == "POST":
        front_image = request.FILES['front']
        back_image = request.FILES['back']
        user = UserProfile.objects.get(id=pk)
        adhar = AadharImage.objects.create(
            front_image=front_image,
            back_image = back_image,
            profile = user)
        return HttpResponse("DOne")

        # return HttpResponse(json.dumps(data), content_type="application/json")

from .adhardata import *

def processAadhar(request, pk):

    user = UserProfile.objects.get(id=pk)
    adhar = AadharImage.objects.get(profile=user)
    data = fetchAllDataFromAadhar(request=request, front_image= adhar.front_image, back_image=adhar.back_image)
    adhar = AadharData.objects.create(profile=user,name=data["name"], 
        dob=data["dob"], 
        sex = data["sex"],
        aadhaar_number = data["aadhaar_number"],
        address = data["address"],
        pincode = data["pincode"],
        netcopy = data['netcopy'])
    return HttpResponse("Done")
