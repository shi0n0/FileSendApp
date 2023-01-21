from django.contrib import admin
from . models import Document
from .models import User

# 管理ツールに登録
admin.site.register(Document)
admin.site.register(User)