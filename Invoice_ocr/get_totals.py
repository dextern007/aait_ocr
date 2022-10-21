# import requests
# import json
# url = "http://38.130.130.45:9595/invoice-ocr/"
# file = open('1.pdf', 'rb')

# payload=json.dumps({'lang': 'eng','document':file.read().decode("utf-8")})

# headers = {
#     "Content-Type":"application/json"
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
from textblob import TextBlob


import datefinder
import spacy
from spacy import matcher
import re
from datetime import date as dt
from datetime import datetime
from nltk import *
from spacy.matcher import Matcher

keywords =["total","balance","subtotal"]


nlp = spacy.load("en_core_web_lg")
# nlp = spacy.load("/media/diwahar/Storage/AAITPRO/aait_ocr/annotation/product_line/model-best")
a=[]
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_ents(line):
        data = dict()
        res =""
        doc = nlp(line)
        for ent in doc.ents:
            res=  ent.label_
            a.append(1)
           
        return res   

# fo = open("annon.txt", "r+")

# lines = fo.readlines()
# print(len(lines))
def get_line_items(lines):
    res=[]
    for i in lines.splitlines():
        i= i.replace("|"," ")
        i= i.replace("\n","")
        i= i.replace("$","")
        i= i.replace("[","")
        i = i.replace("]","")
        i = i.replace("/"," ")
        i = i.replace("-","")
        i = i.replace(":","")
        i = i.replace("#","")
        l=i.split(" ")

        try:
            a = l[-1]
        except:
            pass
        if not has_numbers(a):
            del l[-1]

        try:
            a = l[-1]
        except:
            pass
    
        
        try:
            if l[-1].find(".") != -1 and l[-1][-3]!=",":
                pass
            else:
                a=l[-1].replace(",",".")

        except:
            pass

        try:
            if a[-4]==".":
                a=a.replace(".",",")

        except:
            pass

        try:
            if a[-7]==".":
                a=a.replace(".",",",-7)
        except:
            pass



        if has_numbers(a) and len(l)>2  and (a.find(".") != -1 or a.find(",") != -1):
            l[-1]=a.replace(",","")
            l= " ".join(l)
            
            blob = TextBlob(l)
            list_difference = [item for item in blob.words.lower() if item in keywords]
            # print(list_difference)
            if len(list_difference)!=0:
                # nlp = spacy.load("/media/diwahar/Storage/AAITPRO/aait_ocr/annotation/product_line/model-last")
                # doc=nlp(l)
                # for ent in doc.ents:
                #     print(ent.label_)
                # l2 = []
                # for i in l.split():
                     
                #     l2.append("[ %s ]"%(i))

                # print(l2)
                res.append(l)
                # print(blob)
            else:
                pass
    # print(res)
    return res
# get_line_items(lines)