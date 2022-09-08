
from django.db import models

# Create your models here.
class UImage(models.Model):
    croppedImage = models.ImageField(upload_to = "cropped",blank=True,null=True)

l=(
    ("eng","eng"),
    ("chi_sim","chi_sim"),
)
class PDF(models.Model):
    document  = models.FileField(upload_to="documents",blank=True,null=True)
    image     = models.FileField(upload_to="documents/images",blank=True,null=True)
    launguage = models.CharField(choices=l,max_length=255,blank=True,null=True)
    verified  = models.BooleanField(default=False)
    c_image   = models.ForeignKey(UImage,blank=True,null=True,on_delete=models.CASCADE)
 