
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


class OCRView(APIView):
    def post(self,request,format=None):
        lang = request.data["lang"]
        file = request.data['document']
        # print(file)
        # print(type(file))
        ocr                = Ocr(source_document=base64.b64decode(file.encode('utf-8')))
        extracted_text     = ocr.extract_text(lang=lang)
        launguage_code     = deduct_launguage.get_launguage_code(extracted_text)

        filtered_text_data = ocr.split_lines(extracted_text)



        predictor = Predictor(data=filtered_text_data)

        dates              =   predictor.getall_date()
        names              =   predictor.getall_names()
        organizations      =   predictor.getall_organizations()
        amounts            =   predictor.getall_amounts()
        numbers            =   predictor.getall_numbers()
        product_lines      =   predictor.ProductLines()
        invoice_date       =   predictor.InvoiceDate(dates)
        customer_id        =   predictor.CustomerId()
        customer_name      =   predictor.CustomerName(names)
        vendor_name        =   predictor.VendorName(organizations)
        vendor_location    =   predictor.VendorLocation()
        vendor_address     =   predictor.VendorAddress()
        start_date         =   predictor.StartDate(dates)
        end_date           =   predictor.DueDate(dates)
        invoice_number     =   predictor.InvoiceId()
        vat_code           =   predictor.VendorTaxId()
        untaxed_amount     =   predictor.SubTotal()
        taxes              =   predictor.TotalTax()
        total              =   predictor.InvoiceTotal()
        purchase_order     =   predictor.PurchaseOrder()


        respose = {}
        respose["all_dates"]     = dates
        respose["names"]         = names
        # respose["organizations"] = organizations
        respose["amounts"]       = amounts
        respose["numbers"]       = numbers
        respose["product_lines"] = product_lines
        respose["invoice_date"]  = invoice_date
        respose["customer_id"]   = customer_id
        respose["vendor_name"]   = vendor_name
        respose["vendor_location"]   = vendor_location
        respose["vendor_address"]   = vendor_address
        respose["customer_name"] = customer_name
        respose["invoice_number"]= invoice_number
        respose["start_date"]    = start_date
        respose["end_date"]      = end_date
        respose["vat_code"]      = vat_code
        respose["untaxed_amount"]= untaxed_amount
        respose["taxes"]         = taxes
        respose["total"]         = total
        respose["purchase_order"]= purchase_order


        return Response({"predicted_data":respose,"extracted_text":filtered_text_data})


