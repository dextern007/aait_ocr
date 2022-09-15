
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# from account.models import DeviceVerification,User
from rest_framework.authtoken.models import Token

from django.core.files.images import ImageFile
# import invoice_reader
from Invoice_ocr import deduct_launguage
# import pdfplumber
from Invoice_ocr.ocr import Ocr
# import base64
# import requests, PyPDF2, io
from textblob import TextBlob
import pandas as pd

from Invoice_ocr.predictor import Predictor

import base64

from api.models import UImage
import test

class OCRView(APIView):
    def post(self,request,format=None):
        # return Response({"h":"a"})
        
        lang = request.data["lang"]
        file = request.data['document']
        # file = request.FILES['document']
        # print(file)
        # print(type(file))
        
        text =""


        ocr                = Ocr(source_document=base64.b64decode(file.encode('utf-8')),read_type="bytes")

        extracted_text=ocr.extract_text(lang=lang+"+eng")
        launguage_code     = deduct_launguage.get_launguage_code(extracted_text)
        filtered_text_data = ocr.split_lines(extracted_text,launguage_code)
        predictor = Predictor(data=filtered_text_data)
        out= predictor.get_trained_ents()
        # print(out)
        
        line_items=test.get_line_items(extracted_text["res_two"])
        line_items=predictor.ProductLines(line_items)
        out["line_items"]=line_items
        # print(extracted_text)

        
       
        # ocr                = Ocr(source_document=file.read())
        # extracted_text     = ocr.extract_text(lang=lang)
        # launguage_code     = deduct_launguage.get_launguage_code(extracted_text)

        # filtered_text_data = ocr.split_lines(extracted_text,launguage_code)



        # predictor = Predictor(data=filtered_text_data)

        # dates              =   predictor.getall_date()
        # names              =   predictor.getall_names()
        # organizations      =   predictor.getall_organizations()
        # amounts            =   predictor.getall_amounts()
        # numbers            =   predictor.getall_numbers()
        # product_lines      =   predictor.ProductLines()
        # invoice_date       =   predictor.InvoiceDate(dates)
        # customer_id        =   predictor.CustomerId()
        # customer_name      =   predictor.CustomerName(names)
        # vendor_name        =   predictor.VendorName(organizations)
        # vendor_location    =   predictor.VendorLocation()
        # vendor_address     =   predictor.VendorAddress()
        # start_date         =   predictor.StartDate(dates)
        # end_date           =   predictor.DueDate(dates)
        # invoice_number     =   predictor.InvoiceId()
        # vat_code           =   predictor.VendorTaxId()
        # untaxed_amount     =   predictor.SubTotal()
        # taxes              =   predictor.TotalTax()
        # total              =   predictor.InvoiceTotal()
        # purchase_order     =   predictor.PurchaseOrder()


        # respose = {}
        # respose["all_dates"]     = dates
        # respose["names"]         = names
        # # respose["organizations"] = organizations
        # respose["amounts"]       = amounts
        # respose["numbers"]       = numbers
        # respose["product_lines"] = product_lines
        # respose["invoice_date"]  = invoice_date
        # respose["customer_id"]   = customer_id
        # respose["vendor_name"]   = vendor_name
        # respose["vendor_location"]   = vendor_location
        # respose["vendor_address"]   = vendor_address
        # respose["customer_name"] = customer_name
        # respose["invoice_number"]= invoice_number
        # respose["start_date"]    = start_date
        # respose["end_date"]      = end_date
        # respose["vat_code"]      = vat_code
        # respose["untaxed_amount"]= untaxed_amount
        # respose["taxes"]         = taxes
        # respose["total"]         = total
        # respose["purchase_order"]= purchase_order

        # trained_output = predictor.get_trained_ents()
        return Response(out)


import numpy
from PIL import Image
import pytesseract
import numpy
from django import forms
from Invoice_ocr.ocr import image_processing
import cv2 
def convert_np_image(image):
        pil_image = image.convert('RGB') 
        open_cv_image = numpy.array(pil_image) 
        # image = np.full((300, 300, 3), 255).astype(np.uint8)
        # Convert RGB to BGR 
        img = open_cv_image[:, :, ::-1].copy() 
        return img


class ImageForm(forms.ModelForm):
    class Meta:
        model = UImage
        fields = "__all__"

def pre_process_image(image):
        # image= self.convert_np_image(image)
        gray = image_processing.get_grayscale(image)
        thresh = image_processing.thresholding(gray)
        noise_removal = image_processing.remove_noise(thresh)
        opening = image_processing.opening(gray)
        canny = image_processing.canny(gray)
        erode = image_processing.erode(gray)
        # cv2.imwrite('test.jpg',thresh)
        # cv2.waitKey(0)
        return thresh

import translators as ts
def pre_process_image(image):
    # image= self.convert_np_image(image)
    gray = image_processing.get_grayscale(image)
    thresh = image_processing.thresholding(gray)
    noise_removal = image_processing.remove_noise(thresh)
    opening = image_processing.opening(gray)
    canny = image_processing.canny(gray)
    erode = image_processing.erode(gray)
    # cv2.imwrite('test.jpg',thresh)
    # cv2.waitKey(0)
    return thresh


class CropperOCR(APIView):

    def post(self,request,format=None):
        # import easyocr
        form = ImageForm(request.POST or None ,request.FILES or None)
        if form.is_valid():
            instance = form.save()
            path = instance.croppedImage

        else :
            print(form.errors)

        text = pytesseract.image_to_string(pre_process_image(convert_np_image(Image.open(path))),lang=request.data["lang"]+"+eng",config="--psm 6")
        # print(text)
        text  = ts.google(text,to_language='en')

        return Response({"response":text})