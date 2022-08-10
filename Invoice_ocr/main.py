# import invoice_reader
import deduct_launguage
# import pdfplumber
from ocr import Ocr
# import base64
# import requests, PyPDF2, io
from textblob import TextBlob
import pandas as pd
import datefinder
import spacy
from predictor import Predictor


pdf_path = str(input("Enter the PDF Path : "))
lang =  input("Choose OCR Launguage :")
#  = invoice_reader.get_text(pdf_path)



ocr                = Ocr(source_document=pdf_path)
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
respose["customer_name"] = customer_name
respose["vendor_name"]   = vendor_name
respose["start_date"]    = start_date
respose["end_date"]      = end_date
respose["invoice_number"]= invoice_number
respose["vat_code"]      = vat_code
respose["untaxed_amount"]= untaxed_amount
respose["taxes"]         = taxes
respose["total"]         = total
respose["purchase_order"]= purchase_order


print(respose)
# for i in respose:
#     print(i)
#     print("------------------")
#     for j in respose[i]:
#         print(j)

#     print("------------------")
#     print("\n")




# print({"predicted_data":respose,"extracted_raw_data": filtered_text_data})


# df = pd.DataFrame(filtered_text_list[0])


# # print(filtered_text_list[1])










# print(df)
# print(df["line"])


# for lines in filtered_text_data["result"]:
    
#     print(lines["line"])

# print(filtered_text_list)
# print(launguage_code)
# print(extracted_text)
# from invoice2data import extract_data
# result = extract_data(pdf_path)
# print(result)