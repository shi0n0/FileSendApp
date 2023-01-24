import os
from . import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse
from django_user_agents.utils import get_user_agent
from django.views.generic import View
from core.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.db.models import Q
from .models import Document
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from functools import reduce
from operator import and_
from django.contrib.auth.decorators import login_required
from .forms import UserForm

# アップロードとデリート
def mypage (request):
    return render(request, 'account/mypage.html')

def base (request):
    return render(request, 'base.html')

def detail(request, id):
    detail = Document.objects.get(id=id)
    return render(request, 'core/detail.html', {'detail': detail})

def uploadFile(request):
    if request.method == "POST":
        #form,dataの取得
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]
        content_type = request.FILES["uploadedFile"].content_type

        # データベース保存
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile,
            content_type = uploadedFile.content_type
        )
        document.save()
        print("ファイルをアップロードしました")
        return redirect("/")
        
    documents = models.Document.objects.all()

    return render(request, "core/upload-file.html", context = {
        "files": documents
        })

def delete_file(request,pk):
    template_name = "core/file-delete.html"
    obj = get_object_or_404(models.Document, pk=pk)
    ctx = {"object": obj}
    if request.POST:
        obj.delete()
        print("ファイルを削除しました")
        return redirect("/")
    

    return render(request, template_name, ctx)

#アカウント関連
class AccountCreateView(View):
    def get(self, request):
        return render(request, "account/register.html")

    # post を追加
    def post(self, request):
        # ユーザー情報を保存する
        User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
        )
        # 登録完了画面を表示する
        return render(request, "account/register_success.html")
    



class AccountLoginView(LoginView):
    """ログインページのテンプレート"""
    template_name = 'account/login.html'

    def get_default_redirect_url(self):
        """ログインに成功した時に飛ばされるURL"""
        return "/mypage"
    

class AccountLogoutView(LogoutView):
    template_name = 'account/logout.html'

    def get_default_redirect_url(self):
        """ログアウトに成功した時に飛ばされるURL"""
        return "/mypage"
    

    
class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Document.objects.all()
        keyword = request.GET.get('keyword')

        if keyword:
            query_list = keyword.split()
            query = Q()
            for q in query_list:
                query &= Q(title__exact=keyword)
            post_data = post_data.filter(query)

        return render(request, 'base.html', {
            'keyword': keyword,
            'post_data': post_data
        })
    def id_view(request, id):
        detail = Document.objects.get(id=id)
        file_type = detail.content_type.split('/')[0]
        if detail.content_type.startswith('image'):
            file_type = 'image'
        elif detail.content_type.startswith('video'):
            file_type = 'video'
        elif detail.content_type.startswith('text/plain'):
            file_type = 'text'
        return render(request, 'core/detail.html', {'detail': detail, 'file_type': file_type})
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/mypage')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form})