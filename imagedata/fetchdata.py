import cv2 as cv
import xmltodict
from PIL import Image
from numpy import asarray


def data_from_qr(front_image, back_image):
    try:
        image = Image.open(front_image)
        image = asarray(image)
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
        image = Image.open(back_image)
        image = asarray(image)
        qrCodeDetector = cv.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
        qr_data = decodedText.split(",")[0]
        data_dict = xmltodict.parse(qr_data)
        data = data_dict["PrintLetterBarcodeData"]
        print(data)
        return {"is_data":True, "data": data}
    except:
        return {"is_data":False}