# Generated by Django 3.2 on 2022-09-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_pdf_launguage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='documents/images'),
        ),
    ]
