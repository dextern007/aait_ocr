from distutils.command.upload import upload
from django.db import models

# Create your models here.
class UImage(models.Model):
    croppedImage = models.ImageField(upload_to = "cropped",blank=True,null=True)