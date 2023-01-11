import cv2 as cv
import xmltodict
from PIL import Image
from numpy import asarray
from pytesseract import image_to_string
import requests
import io
from django.conf import settings



class FetchAdhar:
    name = None
    dob = None
    aadhaar_number = None
    address = None
    pincode = None
    netcopy = False

    def update(self, name=None, dob=None, aadhaar_number=None, address=None, picode=None, netcopy=None):
        self.name = name if name else self.name
        self.dob = dob if dob else self.dob
        self.aadhaar_number = aadhaar_number if aadhaar_number else self.aadhaar_number
        self.address = address if address else self.address
        self.pincode = picode if picode else  self.pincode
        self.netcopy = netcopy if netcopy else self.netcopy

    def get_data(self):
        return {
            "name": self.name,
            "dob": self.dob,
            "aadhaar_number": self.adhar_number,
            "address": self.address,
            "pincode": self.pincode}



def numberAndType(image):
    hieght, width = image.shape[0], image.shape[1]
    
    upside = int(hieght/100)*75
    downside = hieght 
    leftside = int(width/5)
    rightside = width-leftside

    img = image[upside:downside, leftside:rightside]

    text = image_to_string(img)
    
    netcopy = False
    
    for keyword in ['vi', 'VI']:
        if keyword in text:
            netcopy = True
            break
    
    adhar_number = ""
    vi_numbercheck = ""
    search_vi = False
    for index in range(len(text)-3):
        try:
            fourdigit = str(text[index]+text[index+1]+text[index+2]+text[index+3])
            if fourdigit.isdigit() and len(fourdigit)==4:
                if search_vi:
                    vi_numbercheck+=fourdigit
                else:
                    adhar_number+=fourdigit
                    if len(adhar_number) >= 12:
                        search_vi = True
                
        except:
            pass
    
    if len(vi_numbercheck) >= 8:
        netcopy = True
    return [adhar_number, netcopy]


def imageToRecords(adhar_obj, front_image, back_image):
    # byte image
    front_data = numberAndType(front_image)
    back__data = numberAndType(back_image)
    netcopy = False
    adhar_number = ""

    if front_data[1] or back__data[1]:
        netcopy = True

    if len(back__data[0]) >= 12:
        adhar_number = back__data[0]
    else:
        adhar_number = front_data[0]

    adhar_obj.update(aadhaar_number=adhar_number, netcopy = netcopy)
    return adhar_obj



def frontImageToRecord(adhar_obj,image):
    hieght, width = image.shape[0], image.shape[1]
    text = image_to_string(image)
    
    upside = int(hieght/100)*18
    downside = hieght - (int(hieght/10)*3)
    leftside = int(width/4)
    rightside = width-leftside
    
    image = image[upside:downside, leftside:rightside]
    text = image_to_string(image)
    print(text)

    lines = text.split('\n')
    text1= []

    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)


    name = None
    sex = None
    dob = ""


    if 'female' in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"


    dob_str = None
    yob_str = None
    for i,data in enumerate(text1):
        if 'DOB' in data or 'DO8' in data:
            dob_str,l = data,i
            name = text1[l-1] if text1[l-1] else text1[l-2]
        elif 'Year' in data:
            yob_str,l = data,i
            name = text1[l-2] if text1[l-2] else text1[l-1]
    if dob_str:
        print("dob_str", dob_str[-10:])
    if yob_str:
        print("yob_str", yob_str)


    if dob_str:
        dob = dob_str[-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace('l', '/')
        dob = dob.replace('L', '/')
        dob = dob.replace('I', '/')
        dob = dob.replace('i', '/')
        dob = dob.replace('|', '/')
        dob = dob.replace('\"', '/1')
        dob = dob.replace(":","")
        dob = dob.replace(" ", "")


    elif yob_str:
        for char in yob_str:
            try:
                int(char)
                dob+=char
            except:
                pass
     
    adhar_obj.update(name=name, dob=dob, sex=sex)
    return adhar_obj


def data_from_qr(front_image, back_image):
    try:
        image = asarray(front_image)
        qrCodeDetector = cv.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
        qr_data = decodedText.split(",")[0]
        data_dict = xmltodict.parse(qr_data)
        data = data_dict["PrintLetterBarcodeData"]
        print(data)
        return {"is_data":True, "data": data}
    except:
        pass

    try:
        image = asarray(back_image)
        qrCodeDetector = cv.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
        qr_data = decodedText.split(",")[0]
        data_dict = xmltodict.parse(qr_data)
        data = data_dict["PrintLetterBarcodeData"]
        print(data)
        return {"is_data":True, "data": data}
    except:
        return {"is_data":False}


def backFirstApproachNetcopy(back_image):

    hieght, width = back_image.shape[0], back_image.shape[1]

    leftside = int(width/2.5)
    rightside = width-leftside
    image = image[0:hieght, 0:rightside]

    text = image_to_string(image)

    lines = text.split('\n')
    text1= []
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
        
        
    def firstWord(adres_line):
        for index, char in enumerate(adres_line):
            if char.isupper():
                return adres_line[index:]
        return adres_line
            
        
    pincode = None
    get_address = False
    is_first = False
    is_last = False
    addres = ""



    def lastWord(adres_line):
        try:
            pin = int(adres_line[-6:])
            return pin
        except:
            return False

    for index, item in enumerate(text1):
        if is_first:
            item = firstWord(item)
            is_first = False
            
        if get_address:
            addres += " "+ item 
                    
        if "Address:" in item:
            is_first = True
            get_address = True
            
        if lastWord(item) and get_address:
            break
            
    pincode = addres[-6:]
    addres
    if addres:
        return True
    False

def backSecondApproachNetcopy(back_image):
    text = image_to_string(back_image)
    lines = text.split('\n')
    text1= []
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
        
        
    def firstWord(adres_line):
        for index, char in enumerate(adres_line):
            if char.isupper():
                return adres_line[index:]
        return adres_line
            
        
    pincode = None
    get_address = False
    is_first = False
    is_last = False
    addres = ""



    def lastWord(adres_line):
        try:
            pin = int(adres_line[-6:])
            return pin
        except:
            return False

    for index, item in enumerate(text1):
        if is_first:
            item = firstWord(item)
            is_first = False
            
        if get_address:
            addres += " "+ item 
                    
        if "Address:" in item:
            is_first = True
            get_address = True
            
        if lastWord(item) and get_address:
            break
            
    pincode = addres[-6:]
    addres
    if addres:
        return True
    return False


def backPostalImage(adhar_obj, back_image):

    hieght, width = back_image.shape[0], back_image.shape[1]
    image = back_image[0:hieght, int(width/2.3):width]

    text = image_to_string(image)
    lines = text.split('\n')
    text1= []
    for lin in lines:
        s = lin.strip()
        s = lin.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)
        
        
    def firstWord(adres_line):
        for index, char in enumerate(adres_line):
            if char.isupper():
                return adres_line[index:]
        return adres_line
            
        
    pincode = None
    get_address = False
    is_first = False
    is_last = False
    addres = ""



    def lastWord(adres_line):
        try:
            pin = int(adres_line[-6:])
            return pin
        except:
            return False

    for index, item in enumerate(text1):
        if "Address:" in item:
            is_first = True
            get_address = True
        
        if is_first:
            item = firstWord(item)
            is_first = False
            
        if get_address:
            addres += " "+ item 
            
        if lastWord(item) and get_address:
            break
            
    pincode = addres[-6:]
    addres = addres[10:]

    adhar_obj.address = addres
    adhar_obj.pincode = pincode
    return adhar_obj


def backImageToRecord(adhar_obj, back_image):
    if adhar_obj.netcopy:
        result = backFirstApproachNetcopy(adhar_obj,back_image)
        if not result:
            result = backSecondApproachNetcopy(adhar_obj,back_image)
            return result
        return result
    else:
        pass



# main function call by user
def fetchAllDataFromAadhar(request, front_image, back_image):
    front_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(front_image)
    back_image_url = "http://" + request.get_host() + settings.MEDIA_URL + str(back_image)

    front_image_file = requests.get(front_image_url)
    back_image_file = requests.get(back_image_url)

    front_image = Image.open(io.BytesIO(front_image.content))
    back_image = Image.open(io.BytesIO(front_image.content))


    adhar_obj = FetchAdhar()

    # 1 from QR Code
    result = data_from_qr(front_image, back_image)
    if result["is_data"]:
        return "Done"
        # return data json format

    # 1 | number, netcopy or not
    adhar_obj = imageToRecords(adhar_obj, front_image,back_image)

    # 2 | front page | name, sex, dob
    adhar_obj = frontImageToRecord(adhar_obj, front_image)
    
    # back_data if internetcopy
    if adhar_obj.netcopy:
        adhar_obj = backImageToRecord(adhar_obj, back_image)
    else:
        pass



