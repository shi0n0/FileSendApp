from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    path("delete/<int:pk>/",views.delete_file, name="delete-file"),
    path("mypage",views.mypage, name="mypage"),
    path("register", views.AccountCreateView.as_view(), name="register"),
    path("login", views.AccountLoginView.as_view(), name="login"),
    path("logout", views.AccountLogoutView.as_view(), name="logout"),
    path("base", views.base, name='base')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)