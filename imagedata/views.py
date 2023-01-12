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
from .adhardata import *




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

    text_f = image_to_string(image_f)
    text_b = image_to_string(image_b)
    text = text_f + text_b
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    data = adhaar_read(text)
    return data


def home(request):
    return render(request, "enternumber.html")


from datetime import datetime

def date_compare(date, date_str):
    datetime_object = datetime.strptime(date_str, '%d/%m/%Y')
    userdata = str(date)
    adhardate = str(datetime_object)[:10]
    result = userdata==adhardate
    return result

def viewdata(request, pk):
    try:
        if request.method == "POST":
            adhar_record = None
            print(request.POST["phone"])
            user = UserProfile.objects.get(phone_number=request.POST["phone"])
            adhar_data = AadharData.objects.filter(profile=user)
            if adhar_data:
                adhar_record = adhar_data[0]
            context = {
                "userdata":user, 
                "adhar_data":adhar_record,
                }
            return render(request, "viewdata.html", context=context)

        if request.method == "GET":
            user = UserProfile.objects.get(id=pk)
            adhar_data = AadharData.objects.filter(profile=user)
            if adhar_data:
                adhar_record = adhar_data[0]
            else:
                adhar_record = None
            context = {
                    "userdata":user, 
                    "adhar_data":adhar_record,
                    }
            return render(request, "viewdata.html",context)

    except:
        return HttpResponse("User does not found")
        


def newdata(request):
    if request.method == "GET":
        return render(request,"userdata.html")

    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        dob = request.POST['dob']
        aadhar_number = request.POST['aadhaar']
        address = request.POST['address']
        pincode = request.POST['pincode']
        sex = request.POST['sex']

        # userprofile
        userprofile = UserProfile(name=name,
            dob=dob,
            aadhaar_number=aadhar_number,
            address = address,
            pincode = pincode,
            sex = sex,
            phone_number=phone)
        userprofile.save()
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
        url = f"/viewdata/{user.id}/"
        return redirect(url)


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

    adhar.is_name_matched = user.name.lower() == adhar.name.lower()
    adhar.is_adhar_matched = user.aadhaar_number == adhar.aadhaar_number 
    adhar.is_pincode_matched = user.pincode == adhar.pincode
    adhar.is_sex_matched = user.sex == adhar.sex
    adhar.is_dob_matched = date_compare(user.dob, adhar.dob)
    adhar.save()
            
    url = f"/viewdata/{user.id}/"
    return redirect(url)

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from urllib.request import urlopen
from PIL import Image
import io
from io import StringIO 
import base64
import cv2
from PIL import Image
from PIL import ImageDraw
from django.core.files.uploadedfile import InMemoryUploadedFile




def upload_face(request, pk):
    if request.method == "GET":
        user = UserProfile.objects.get(id=pk)
        return render(request, "faceupload.html", {"userdata":user})
    if request.method == "POST":
        user = UserProfile.objects.get(id=pk)
        image_path = request.POST["src"]

        decodedData = base64.b64decode((image_path[21:]))
        image = Image.open(io.BytesIO(decodedData))

        # buffer = str(StringIO())

        # image.save(buffer, "PNG")

        # image_file = InMemoryUploadedFile(buffer, None, 'test.png', 'image/png', len(buffer), None)

        # print(image_file)

        # user.pic = ('test.png', image_file)
        # user.save()

        # print(decodedData)



        
        # print(image_path)
        return HttpResponse(image_path)
