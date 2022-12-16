from django.db import models

# Create your models here.

#アップロードされたファイルの詳細
class Document(models.Model):
    title = models.CharField(max_length = 10)
    uploadedFile = models.FileField(max_length = 100 , upload_to = "UploadedFiles/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
