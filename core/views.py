from . import models
from django.shortcuts import render

# Create your views here.
def uploadFile(request):
    if request.method == "POST":
        #form,dataの取得
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # データベース保存
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "core/upload-file.html", context = {
        "files": documents
    })