from django import forms # Djangoのformsモジュールをインポート

# SearchFormクラスを定義
class SearchForm(forms.Form):
        keyword = forms.CharField(label='', max_length=50)