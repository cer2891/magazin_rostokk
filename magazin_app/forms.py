# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Category
from .models import Cart
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={"class": "form-control"})
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}
    ))
    captcha = CaptchaField()


class NewForm(forms.ModelForm):
    class Meta:
        model = Cart
        # fields= '__all__'
        fields = ['title','content',  'category', 'photo_urll',
                  'price', 'number', 'is_published',]
        # labels = {'title' : 'Новое', }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"},),
            'content': forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }),
            'category': forms.Select(attrs={"class": "form-control"}),
            'photo_urll': forms.URLInput(attrs={"class": "form-control"}),
        }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if re.match(r'\d', title):
    #         raise ValidationError('Название не должно начинатся с цифры')
    #     return title

