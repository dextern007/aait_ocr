
import re
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
        cv2.imwrite("crop.jpg",cropped_image)
        
        # return {"top":top,"bottom":bottom}

    def pre_process_image(self,image):
        # image= self.convert_np_image(image)
        gray = image_processing.get_grayscale(image)
        thresh = image_processing.thresholding(gray)
        noise_removal = image_processing.remove_noise(thresh)
        opening = image_processing.opening(gray)
        canny = image_processing.canny(gray)
        erode = image_processing.erode(gray)
        cv2.imwrite('test.jpg',thresh)
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
    
    def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
    
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
    
            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(x) + ',' +
                        str(y), (x,y), font,
                        1, (255, 0, 0), 2)
            cv2.imshow('image', img)
    
        # checking for right mouse clicks    
        if event==cv2.EVENT_RBUTTONDOWN:
    
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
    
            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            cv2.putText(img, str(b) + ',' +
                        str(g) + ',' + str(r),
                        (x,y), font, 1,
                        (255, 255, 0), 2)
            cv2.imshow('image', img)

    def extract_text(self,lang):
        response = ""
        full_response = ""
        images = convert_to_image.get_images(self.source_document)
        
        
        for i in range(len(images)):
           
            border_removed_image = image_processing.remove_border_lines(image=self.convert_np_image(images[i]))
           

            thresh = self.pre_process_image(border_removed_image)
            # self.crop_image(thresh)
            thresh_one = self.pre_process_image(self.convert_np_image(images[i]))
            
            # osd = self.osd(thresh)
            split_image = self.split_images(thresh)
            # top_export_data = self.export_data(split_image["top"],lang=lang)
            # top_boxed_image = self.image_to_box(split_image["top"],top_export_data,"top")
            # bottom_export_data = self.export_data(split_image["bottom"],lang=lang)
            # bottom_boxed_image = self.image_to_box(split_image["bottom"],bottom_export_data,"bottom")
            top_part = pytesseract.image_to_string(split_image["top"],lang=lang,config=custom_config)
            
            bottom_part = pytesseract.image_to_string(split_image["bottom"],lang=lang,config=custom_config)
            text = top_part+"\n"+bottom_part+"\n"    
            full_text = pytesseract.image_to_string(thresh_one,lang=lang)

            full_response = full_response+full_text+"\n"
            response=response+text+"\n" 
       
        
        return {"res_one":full_response,"res_two":response}

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

    def split_lines(self,ntxt,lang):
        full_txt = self.remove_empty_lines(ntxt["res_one"])
        part_txt = self.remove_empty_lines(ntxt["res_two"])
        full_txt = ts.google(full_txt,to_language='en')
        part_txt = ts.google(part_txt,to_language='en')
        txt = full_txt+"\n"+"EXTRACTION METHOD 2"+"\n"+part_txt
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
