import datefinder
import spacy
from spacy import matcher
import re
from datetime import date as dt
from datetime import datetime
from spacy.matcher import Matcher

class Predictor:

    def __init__(self,data):
        self.data = data
        # self.nlp = spacy.load("/home/diwahar/Work/aait_ocr/annotation/train/model-last")
        self.nlp = spacy.load("en_core_web_lg")
        self.matcher = Matcher(self.nlp.vocab)

 
    def on_match(self,matcher, doc, id, matches):
        print('Matched!', matches)

        
    def test_match(self,):
        patterns = [
        [{"ORTH": "invoice"}, {"ORTH": "number"},{"ORTH": "date"} , {"ORTH": "Date"}, {"ORTH": "email"}]
        ]
        self.matcher.add("TEST_PATTERNS", patterns, on_match=self.on_match)
        doc = self.nlp(self.data["txt"])
        matches = self.matcher(doc)

    def get_trained_ents(self):
        nlp = spacy.load("/media/diwahar/Storage/AAITPRO/aait_ocr/annotation/train/model-best")
        # nlp = spacy.load("en")
        data = dict()
        l=[
        "CUSTOMER_NAME", #Required
        "VENDOR_NAME", #Required
        "INVOICE_NUMBER", #Required
        "INVOICE_DATE", #Required
        "DUE_DATE",
        "PO_NUMBER", #Required

        "SUB_TOTAL", #Required
        "TAX_AMOUNT", 
        "TOTAL_AMOUNT", #Required
        "CURRENCY", #Required
        "VAT_NUMBER",

        # "CURRENCY_RATE",

        # "VENDOR_ADDRESS",
        # "VENDOR_WEBSITE",
        # "VENDOR_MOBILE",
        # "VENDOR_EMAIL",
        
        
       
       
        
        

        

        ]


        
        # l = ["INVOICE_NUMBER","PURCHASE_ORDER","PRODUCT_LINE","INVOICE_DATE","VENDOR_NAME","VENDOR_ADDRESS","CUSTOMER_NUMBER","VAT_NUMBER","TOTAL","SUB_TOTAL","TAX","VENDOR_WEBSITE","VENDOR_MOBILE","VENDOR_EMAIL","CURRENCY","DESCRIPTION","END_DATE"]
        for i in l:
            data[i] = ""
        doc = nlp(self.data["txt"])
        for ent in doc.ents:
            
            data[ent.label_] = ent.text
        
        return data

    def get_ents(self):
        data = dict()
        doc = self.nlp(self.data["txt"])
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)

    def getall_date(self):
        matches = list(datefinder.find_dates(self.data["txt"]))
        res = []
        todays_date = dt.today()
        if len(matches) > 0:
            for date in matches:
                if int(date.year) > 1900 and int(date.year)<= int(todays_date.year):
                    res.append(str(date.date()))
        else:
            pass

        return list(tuple(res))


    def getall_names(self):

        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        res = []
        doc = self.nlp(self.data["txt"])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                res.append(ent.text)

        
        return res
            
            


    
    def getall_amounts(self):
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        res = []
        doc = self.nlp(self.data["txt"])
        for ent in doc.ents:
            if ent.label_ == "MONEY":
                res.append(re.sub(",","",ent.text))

            if ent.label_ == "CARDINAL" and ent.text.find(",")>=0:
                res.append(re.sub(",","",ent.text))

            if ent.label_ == "CARDINAL" and ent.text.find(".")>=0:
                res.append(re.sub(",","",ent.text))

        
        return res


            

        
    def getall_organizations(self):
        res = []
        doc = self.nlp(self.data["txt"])
        for ent in doc.ents:
            if ent.label_ == "ORG":
                res.append(ent.text)
        return res

    def getall_numbers(self):
        res = []
        doc = self.nlp(self.data["txt"])
        for ent in doc.ents:
            if ent.label_ == "CARDINAL" and ent.text.find(",")<0:
                res.append(ent.text)
        return res


    def ProductLines(self,lines):
       
        product_lines = [
            "LINE", 
            "PARTICLE_NUMBER", # UNIQUE ONE
            # "PO_NUMBER",
            "DESCRIPTION", #Required
            "QUANTITY",
            "UOM",
            "UNIT_PRICE",
            "TOTAL_AMOUNT", #Required
        ]
        
        res = []
        nlp = spacy.load("/media/diwahar/Storage/AAITPRO/aait_ocr/annotation/product_line/model-best")
        
        for i in lines:
            # print(i)
            data = dict()
            for j in product_lines:
                data[j] = ""
            doc = nlp(i)
            # print(i)
            for ent in doc.ents:
                
                data[ent.label_] = ent.text

            res.append(data)
        # print(res)

        return res


    def CustomerName(self,names):
        res = []
        if len(names) != 0:
            res.append(names[0])
        if len(names) == 2:
            res.append(names[1])
        return res

    def CustomerId(self):
        res = []
        lines = self.data["result"]
        for line in lines:
            if line["line"].lower().find("cust")>=0 and (line["line"].lower().find("id")>=0 or line["line"].lower().find("no")>=0 or line["line"].lower().find("nu")>=0):
                doc = self.nlp(line["line"])
               
                for ent in doc.ents:
                    # print(ent.text,ent.label_)
                    if ent.label_ == "CARDINAL" or ent.label_ == "DATE" and ent.text.find(",")<0:
                        res.append(ent.text)

        return res

    def PurchaseOrder(self):
        res = []
        lines = self.data["result"]
        for line in lines:
            if line["line"].lower().find("po")>=0 or line["line"].lower().find("pur")>=0:
                doc = self.nlp(line["line"])
               
                for ent in doc.ents:
                    # print(ent.text,ent.label_)
                    if ent.label_ == "CARDINAL" or ent.label_ == "DATE" and ent.text.find(",")<0:
                        res.append(ent.text)

        return res
   

    def InvoiceId(self):
        res = []
        lines = self.data["result"]
        for line in lines:
            if line["line"].lower().find("invo")>=0  and (line["line"].lower().find("id")>=0 or line["line"].lower().find("no")>=0 or line["line"].lower().find("nu")>=0 or line["line"].lower().find("invoice")>=0):


          
                doc = self.nlp(line["line"])
                for ent in doc.ents:
                    # print(ent.text,ent.label_)
                    if ent.label_ == "CARDINAL" or ent.label_ == "DATE" and ent.text.find(",")<0:
                        res.append(ent.text)


        numbers = self.getall_numbers()
        for num in numbers:
            if len(num)==8 or len(num)==9:
                res.append(num)

        return res

    def InvoiceDate(self,dates):
        lines = self.data["result"]
        res = []

        for line in lines:
            matches = list(datefinder.find_dates(line["line"]))
            if line["line"].lower().find("invo")>=0  or line["line"].lower().find("date")>=0 :
          
                todays_date = dt.today()
                if len(matches) > 0:
                    for date in matches:
                        if int(date.year) > 1900 and int(date.year)<= int(todays_date.year):
                            res.append(str(date.date()))
                else:
                    pass


        numbers = self.getall_numbers()
        for num in numbers:
            if len(num)==8 or len(num)==9:
                res.append(num)

        return res

    def DueDate(self,dates):
        lines = self.data["result"]
        res = []

        for line in lines:
            matches = list(datefinder.find_dates(line["line"]))
            if line["line"].lower().find("due")>=0  or line["line"].lower().find("date")>=0 :
          
                todays_date = dt.today()
                if len(matches) > 0:
                    for date in matches:
                        if int(date.year) > 1900 and int(date.year)<= int(todays_date.year):
                            res.append(str(date.date()))
                else:
                    pass


        numbers = self.getall_numbers()
        for num in numbers:
            if len(num)==8 or len(num)==9:
                res.append(num)

        return res
    
    def StartDate(self,dates):
        res = []
        return res

    def VendorName(self,orgs):
        return orgs

    def VendorTaxId(self):
        res = []
        lines = self.data["result"]
        for line in lines:
            if line["line"].lower().find("vat")>=0:
                doc = self.nlp(line["line"])
                for ent in doc.ents:
                    # print(ent.text,ent.label_)
                    if ent.label_ == "CARDINAL" or ent.label_ == "DATE" and ent.text.find(",")<0:
                        res.append(ent.text)


        

        return res

    def VendorLocation(self):
        res = []
        lines = self.data["result"]
        for line in lines:
            
            doc = self.nlp(line["line"])
            for ent in doc.ents:
                # print(ent.text,ent.label_)
                if ent.label_ == "GPE":
                    res.append(ent.text)

        return res



    def VendorAddress(self):
        address_regex =["^(\d+) ?([A-Za-z](?= ))? (.*?) ([^ ]+?) ?((?<= )APT)? ?((?<= )\d*)?$" ,
         "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}",
         ]
        res = []

        for regex in address_regex:
            address = re.findall(regex, self.data["txt"])
            res.append(address)

        return res


    def CustomerAddress(self):
        res = []
        return res

    def CustomerTaxId(self):
        res = []
        return res

    def CustomerAddressRecipient(self):
        res = []
        return res

    def BillingAddress(self):
        res = []
        return res

    def BillingAddressRecipient(self):
        res = []
        return res

    def ShippingAddress(self):
        res = []
        return res

    def ShippingAddressRecipient(self):
        res = []
        return res

    def PaymentTerm(self):
        res = []
        return res

    def SubTotal(self):
        res = []
        return res

    def TotalTax(self):
        res = []
        return res

    def TotalVAT(self):
        res = []
        return res

    def InvoiceTotal(self):
        res = []
        return res

    def AmountDue(self):
        res = []
        return res

    def ServiceAddress(self):
        res = []
        return res

    def ServiceAddressRecipient(self):
        res = []
        return res

    def RemittanceAddress(self):
        res = []
        return res

    def RemittanceAddressRecipient(self):
        res = []
        return res

    def ServiceStartDate(self):
        res = []
        return res

    def ServiceEndDate(self):
        res = []
        return res

    def PreviousUnpaidBalance(self):
        res = []
        return res


    