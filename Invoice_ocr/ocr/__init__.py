import re
from numpy import source
from pdf2image import convert_from_bytes,convert_from_path
from Invoice_ocr.ocr import convert_to_image
from PIL import Image
import pytesseract
from pytesseract import Output
import pandas as pd
import cv2
import translators as ts
import numpy
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


custom_config = r"""Arabic
+Armenian
+Bengali
+Canadian_Aboriginal
+Cherokee
+Cyrillic
+Devanagari
+Ethiopic
+Fraktur
+Georgian
+Greek
+Gujarati
+Gurmukhi
+HanS
+HanS_vert
+HanT
+HanT_vert
+Hangul
+Hangul_vert
+Hebrew
+Japanese
+Japanese_vert
+Kannada
+Khmer
+Lao
+Latin
+Malayalam
+Myanmar
+Oriya
+Sinhala
+Syriac
+Tamil
+Telugu
+Thaana
+Thai
+Tibetan
+Vietnamese
+afr
+amh
+ara
+asm
+aze
+aze_cyrl
+bel
+ben
+bos
+bod
+bre
+bul
+cat
+ceb
+ces
+chi_sim
+chi_sim_vert
+chi_tra
+chi_tra_vert
+chr
+cos
+cym
+dan
+deu
+div
+dzo
+ell
+eng
+enm
+epo
+est
+eus
+fao
+fas
+fil
+fin
+fra
+frk
+frm
+fry
+gla
+gle
+glg
+grc
+guj
+hat
+heb
+hin
+hrv
+hun
+hye
+iku
+ind
+isl
+ita
+ita_old
+jav
+jpn
+jpn_vert
+kan
+kat
+kat_old
+kaz
+khm
+kir
+kmr
+kor
+kor_vert
+lao
+lat
+lav
+lit
+ltz
+mal
+mar
+mkd
+mlt
+mon
+mri
+msa
+mya
+nep
+nld
+nor
+oci
+ori
+osd
+pan
+pol
+por
+pus
+que
+ron
+rus
+san
+sin
+slk
+slv
+snd
+spa
+spa_old
+sqi
+srp
+srp_latn
+sun
+swa
+swe
+syr
+tam
+tat
+tel
+tgk
+tha
+tir
+ton
+tur
+uig
+ukr
+urd
+uzb
+uzb_cyrl
+vie
+yid
+yor --psm 6
"""

class Ocr:


    def __init__(self,source_document):
        self.source_document = source_document

    def pre_process_image(self,image):
        """This function will pre-process a image with: cv2 & deskew
        so it can be process by tesseract"""

        pil_image = image.convert('RGB') 
        open_cv_image = numpy.array(pil_image) 
        # Convert RGB to BGR 
        img = open_cv_image[:, :, ::-1].copy() 
        # img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #change color format from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #format image to gray scale
        # kernel = numpy.ones((1, 1), numpy.uint8)
        # img = cv2.dilate(img, kernel, iterations=1)
        # img = cv2.erode(img, kernel, iterations=1)
        # cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        
        # cv2.imshow(img)
        return img

    
    def extract_text(self,lang):
        # chinese_w_1
        response = ""
        images = convert_to_image.get_images(self.source_document)

        
        for image in images:
            # thresh = self.pre_process_image(image)
            thresh = image
            if lang == "":
                text = pytesseract.image_to_string(thresh,config=custom_config)
            else:
                text = pytesseract.image_to_string(thresh,config=custom_config,lang=lang)

            # print(d)

            

            response=response+text+"\n" 
       

        # script_name, confidence = self.detect_image_lang(image)

        # print(script_name,confidence)
        # print(response)
        return response


    def detect_image_lang(self,img_path):
        try:
            osd = pytesseract.image_to_osd(img_path)
            script = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
            conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
            return script, float(conf)
        except:
            return None, 0.0


    def remove_empty_lines(self,txt):
        res=""
        l=[x for x in txt.splitlines() if x!=" " and x!="" and x != None ]
        for i in l:
            res=res+i+"\n"
        return res


    def split_lines(self,txt):
        txt = self.remove_empty_lines(txt)
        txt = ts.google(txt, to_language='en')
        res = []
        # tokenizer = RegexpTokenizer(r'\w+')
        # words = tokenizer.tokenize(txt)
        words = word_tokenize(txt)
        text_to_list = [x for x in txt.splitlines()]
        for i in range(len(text_to_list)):
            index = i
            line  = text_to_list[i]
            tokenized_line = word_tokenize(text_to_list[i])
            res.append({
                "index": i,
                "line" : line,
                "tokenized_line": tokenized_line
            })

        return {"result":res , "words":words , "txt":txt}
        

