
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import pytesseract
import numpy





def predictImage(request):
    text =""
    if request.method == "POST":
        # print(request.POST)
        fileObj = request.FILES['cropped_result']
        text = pytesseract.image_to_string(convert_np_image(fileObj))
        
    return render(request, 'cropper.html',{"k":text})
