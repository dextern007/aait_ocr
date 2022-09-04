
from multiprocessing.connection import wait
import re
from time import sleep
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
from Invoice_ocr.ocr import image_processing

# from deep_translator import *
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
+yor --psm 10
"""


templates = {

    #chinese handwritten
    "one":[
        [228, 312, 281, 1033],
        [322, 413, 278, 1033],
        [327, 409, 1016, 1739],
        [584, 642, 1670, 1985],
        [585, 664, 1308, 1517],
        [1012, 1091, 1324, 1489],
        [1115, 1173, 1344, 1524],
        [1224, 1308, 1329, 1524],
    ],
    #Han Tai
    "two" : [
        [72, 159, 159, 546],
        [137, 200, 664, 1072],
        [181, 224, 210, 418],
        [231, 294, 217, 587],
        [289, 342, 219, 398],
        [470, 536, 1481, 1607],
        [864, 917, 1031, 1159],
        [1014, 1062, 1039, 1155],
        [939, 992, 1063, 1159],
        [1038, 1127, 1324, 1633],
        [927, 980, 1321, 1515],
    ],

    #Crane Rental
    "three":[
        [138, 302, 388, 877],
        [290, 411, 156, 495],
        [65, 370, 884, 1572],
        [993, 1075, 1400, 1736],
        [709, 745, 313, 463],
    ],

    # Hitec
    "four":[
        [67, 125, 1074, 1439],
        [118, 265, 1074, 1466],
        [365, 553, 849, 1485],
        [698, 882, 77, 554],
        [650, 858, 1057, 1613],
        [2059, 2262, 970, 1592],
        [1638, 1916, 788, 1773],
    ],

    # Miratec
    "five":[
        [47, 109, 995, 1309],
        [106, 322, 656, 1663],
        [172, 318, 184, 581],
        [1568, 1602, 261, 413],
        [1840, 2093, 1147, 1702],
    ],

    "six":[
        [580, 626, 46, 216],
        [370, 515, 544, 955],
        [541, 643, 543, 975],
        [652, 758, 544, 953],
        [787, 915, 541, 970],
        [278, 367, 1493, 1957],
        [539, 592, 100, 445],
    ],
    "seven":[
        [50, 123, 579, 1094],
        [111, 171, 650, 993],
        [161, 219, 722, 978],
        [200, 263, 210, 459],
        [268, 323, 227, 579],
        [331, 389, 227, 401],
        [507, 546, 1469, 1568],
        [2000, 2041, 1109, 1227],
        [2126, 2172, 1116, 1227],
        [2145, 2285, 1222, 1652],
        [2056, 2133, 1302, 1660],
        [2000, 2041, 1246, 1602],
        [369, 444, 1109, 1578],
        [181, 268, 50, 439],
    ],
    "eight":[
        [149, 379, 515, 1146],
        [157, 360, 1158, 1564],
        [707, 785, 1020, 1308],
        [971, 1007, 471, 606],
        [990, 1058, 1453, 1557],
    ]
}

positions = [
       [228, 312, 281, 1033],
        [322, 413, 278, 1033],
        [327, 409, 1016, 1739],
        [584, 642, 1670, 1985],
        [585, 664, 1308, 1517],
        [1012, 1091, 1324, 1489],
        [1115, 1173, 1344, 1524],
        [1224, 1308, 1329, 1524],
        [72, 159, 159, 546],
        [137, 200, 664, 1072],
        [181, 224, 210, 418],
        [231, 294, 217, 587],
        [289, 342, 219, 398],
        [470, 536, 1481, 1607],
        [864, 917, 1031, 1159],
        [1014, 1062, 1039, 1155],
        [939, 992, 1063, 1159],
        [1038, 1127, 1324, 1633],
        [927, 980, 1321, 1515],
        [138, 302, 388, 877],
        [290, 411, 156, 495],
        [65, 370, 884, 1572],
        [993, 1075, 1400, 1736],
        [709, 745, 313, 463],
        [67, 125, 1074, 1439],
        [118, 265, 1074, 1466],
        [365, 553, 849, 1485],
        [698, 882, 77, 554],
        [650, 858, 1057, 1613],
        [2059, 2262, 970, 1592],
        [1638, 1916, 788, 1773],
        [47, 109, 995, 1309],
        [106, 322, 656, 1663],
        [172, 318, 184, 581],
        [1568, 1602, 261, 413],
        [1840, 2093, 1147, 1702],
        [580, 626, 46, 216],
        [370, 515, 544, 955],
        [541, 643, 543, 975],
        [652, 758, 544, 953],
        [787, 915, 541, 970],
        [278, 367, 1493, 1957],
        [539, 592, 100, 445],
        [50, 123, 579, 1094],
        [111, 171, 650, 993],
        [161, 219, 722, 978],
        [200, 263, 210, 459],
        [268, 323, 227, 579],
        [331, 389, 227, 401],
        [507, 546, 1469, 1568],
        [2000, 2041, 1109, 1227],
        [2126, 2172, 1116, 1227],
        [2145, 2285, 1222, 1652],
        [2056, 2133, 1302, 1660],
        [2000, 2041, 1246, 1602],
        [369, 444, 1109, 1578],
        [181, 268, 50, 439],
        [149, 379, 515, 1146],
        [157, 360, 1158, 1564],
        [707, 785, 1020, 1308],
        [971, 1007, 471, 606],
        [990, 1058, 1453, 1557],
]

bottom = [
   
]

class Ocr:

    def __init__(self,source_document):
        self.source_document = source_document

    def convert_np_image(self,image):
        pil_image = image.convert('RGB') 
        open_cv_image = numpy.array(pil_image) 
        # image = np.full((300, 300, 3), 255).astype(np.uint8)
        # Convert RGB to BGR 
        img = open_cv_image[:, :, ::-1].copy() 
        return img

    def crop_image(self,image):
        h, w  = image.shape
        cropped_image = image[348:248+h,359:359+w]
        # cv2.imwrite("crop.jpg",cropped_image)
        
        # return {"top":top,"bottom":bottom}

    def pre_process_image(self,image):
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

    def osd(self,image):
        print(pytesseract.image_to_osd(image))

    def image_to_box(self,image,d,name):
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(float(d['conf'][i])) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite(name+'.jpg', image)

      
    def export_data(self,image,lang,):
        d = pytesseract.image_to_data(image, output_type=Output.DICT)
        return d
           
    def split_images(self,img):
        h, w  = img.shape
        half = w//2
        left_part = img[:, :half] 
        right_part = img[:, half:]  
        half2 = h//2
        top = img[:half2, :]
        bottom = img[half2:, :]
        cv2.imwrite("top.jpg",top)
        cv2.imwrite("bottom.jpg",bottom)
        return {"top":top,"bottom":bottom}
    
   

    def extract_text(self,lang):
        l=[]
        response = ""
        full_response = ""
        images = convert_to_image.get_images(self.source_document)
        
        
        for i in range(len(images)):
           
            border_removed_image = self.convert_np_image(images[i])
            # border_removed_image = image_processing.remove_border_lines(image=self.convert_np_image(images[i]))
            thresh = self.pre_process_image(border_removed_image)
            # print(self.detect_image_lang(thresh))
            # cv2.imwrite(str(i)+".jpg", thresh)
           
            for ax in positions:
                
                try:
                    # cv2.imwrite("crop.jpg",thresh[ax[0]:ax[1],ax[2]:ax[3]])
                    extraction = pytesseract.image_to_string(thresh[ax[0]:ax[1],ax[2]:ax[3]],lang=lang,config=custom_config)
                    response = response+extraction+"\n"
                    
                    # sleep(1)
                except:
                    pass
            
            
           
                
           
            # self.crop_image(thresh)
            # thresh_one = self.pre_process_image(self.convert_np_image(images[i]))
            
            # osd = self.osd(thresh)
            # split_image = self.split_images(thresh)
            # # top_export_data = self.export_data(split_image["top"],lang=lang)
            # # top_boxed_image = self.image_to_box(split_image["top"],top_export_data,"top")
            # # bottom_export_data = self.export_data(split_image["bottom"],lang=lang)
            # # bottom_boxed_image = self.image_to_box(split_image["bottom"],bottom_export_data,"bottom")
            # top_part = pytesseract.image_to_string(split_image["top"],lang=lang,config=custom_config)
            
            # bottom_part = pytesseract.image_to_string(split_image["bottom"],lang=lang,config=custom_config)
            # text = top_part+"\n"+bottom_part+"\n"    
            # full_text = pytesseract.image_to_string(thresh_one,lang=lang)

            # full_response = full_response+full_text+"\n"
            # response=response+text+"\n" 
       
       
        return {"res_two":response}

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
        filtered = filter(lambda x: not re.match(r'^\s*$', x), txt.splitlines())
       
        for i in filtered:
            res=res+i+"\n"
        return res

    def split_lines(self,ntxt,lang):
        part_txt = self.remove_empty_lines(ntxt["res_two"]).splitlines()
        # print(part_txt)
        txt  = ""
        for line in part_txt:
            try:
                res = ts.google(line,to_language='en')
                txt = txt+res+"\n"
            except:
                pass

        # txt = part_txt
        # translated = MicrosoftTranslator(source='auto', target='de').translate(txt)
        # print(translated)
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
        

# Easy OCR
    def extract_easy_ocr(self,image):
        import easyocr
        res = ""
        reader = easyocr.Reader(['ch_tra','en']) # this needs to run only once to load the model into memory
        result = reader.readtext(self.pre_process_image(image),detail = 0, paragraph=True)
        for i in result:
            res=res+i+"\n"

        txt = ts.google(res,to_language='en')
        print(txt)   
