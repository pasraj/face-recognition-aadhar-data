from django.shortcuts import render
from django.http import HttpResponse

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


# def hello(request):
#     users = UserTable.objects.filter(is_updated=False)
#     for user in users:
#         
#         front_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(user.front)
#         data = read_image(front_image_url,back_image_url)
#         adhar = Adhaar(name=data["Name"],dob=data["Dob"],
#             adhar_number=data["AdhaarNumber"],
#             address = data["Address"],
#             sex=data["Sex"])
#         try:
#             current_user = UserTable.objects.get(id=user.id)
#             current_user.is_updated = True
#             current_user.save()
#             adhar.save()
#         except:
#             pass
#     return HttpResponse("Task is done")

