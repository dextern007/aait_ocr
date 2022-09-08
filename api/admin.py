from django.contrib import admin
from api.models import *
# Register your models here.
from django.utils.html import format_html

class PDFAdmin(admin.ModelAdmin):
    list_filter  = ["verified"]
    list_display = ["pk","document","image","launguage","verified","ocr_link"]
    list_editable= ["launguage","verified"]

    def ocr_link(self, obj):
        return format_html(
 '<a target="_blank"  href="/cropper/{0}" >Open</a>&nbsp;',
            obj.pk
        )

    ocr_link.short_description = 'Link'
    ocr_link.allow_tags = True

admin.site.register(PDF,PDFAdmin)