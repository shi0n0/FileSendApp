from django import forms # Djangoのformsモジュールをインポート
from .models import User

# プロフィール編集用
class UserForm(forms.ModelForm):
        class Meta:
                model = User
                fields = ['username','bio']

# SearchFormクラスを定義
class SearchForm(forms.Form):
        keyword = forms.CharField(label='', max_length=50)

class LikeForm(forms.Form):
        content = forms.CharField()

class DislikeForm(forms.Form):
        content = forms.CharField()