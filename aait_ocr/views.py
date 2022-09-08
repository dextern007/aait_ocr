
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
from api.views import convert_np_image
from django import forms
from api.models import *
from Invoice_ocr import deduct_launguage
from Invoice_ocr.predictor import Predictor


def predictImage(request,pk):
    text =""
    from Invoice_ocr.ocr import Ocr
    pdf =PDF.objects.get(pk=pk)
    ocr =Ocr(source_document=pdf.document.path)
    extracted_text=ocr.extract_text(lang=pdf.launguage+"+eng")
    launguage_code     = deduct_launguage.get_launguage_code(extracted_text)
    filtered_text_data = ocr.split_lines(extracted_text,launguage_code)
    predictor = Predictor(data=filtered_text_data)
    out= predictor.get_trained_ents()
    # print(out)

    pdf = PDF.objects.get(pk=pk)
    if request.method == "POST":
        # print(request.POST)
        fileObj = request.FILES['cropped_result']
        text = pytesseract.image_to_string(convert_np_image(fileObj))
        
    return render(request, 'cropper.html',{"k":text,"pdf":pdf,"out":out})

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ["document","launguage"]

class ImageForm(forms.ModelForm):
    class Meta:
        model = UImage
        fields = "__all__"

from pdf2image import convert_from_bytes,convert_from_path

def get_document_image(src):

    image_list = []
    images = convert_from_path(src)
    
    for image in images:
        image_list.append(image)
        # print(image)

    return image_list[-1]

from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
from django.core.files import File
from django.core.files.base import ContentFile
import cv2

def UploadPDF(request):
    text =""
    
    if request.method == "POST":
        # print(request.POST)
        form = PDFForm(request.POST or None ,request.FILES or None)
        if form.is_valid():
            instance = form.save()

            path = instance.document.path
            image = convert_np_image(get_document_image(path))
            pdf = PDF.objects.get(id=instance.id)
            ret, buf = cv2.imencode('.jpg', image)
            content = ContentFile(buf.tobytes())
            pdf.image.save('output.jpg', content)
            

    form = PDFForm(request.POST or None ,request.FILES or None)
    return render(request, 'pdf.html',{"k":text,"form":form})
