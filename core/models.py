import os
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

#アップロードされたファイルの詳細

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 30)
    uploadedFile = models.FileField(max_length = 100 , upload_to = "UploadedFiles/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
    content_type = models.CharField(max_length=255,default="", blank=True, null=True)
    thumbnail = ImageSpecField(source='uploadedFile', processors=[ResizeToFill(100,100)], format='JPEG', options={'quality': 60})
    description = models.CharField(max_length=255,default="", blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    tag1 = models.CharField(max_length=10)
    tag2 = models.CharField(max_length=10)
    tag3 = models.CharField(max_length=10)

    def file_name(self): #ファイル名の抽出
        return os.path.basename(self.uploadedFile.name)
    
class Comment(models.Model):
    name = models.CharField(max_length=50, default="名無しさん", blank=True, null=True)
    body = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

#カスタムユーザーモデル
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Emailを入力して下さい')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self.create_user(username, email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=25, validators=[username_validator], blank=True)
    email = models.EmailField(_("email_address"), unique=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    bio = models.TextField(_("bio"), null=False, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)