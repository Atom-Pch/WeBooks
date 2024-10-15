from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        reg_email = self.cleaned_data.get('email')
        if User.objects.filter(email=reg_email).exists():
            raise ValidationError("A user with that email already exists")

        return reg_email

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class RequestBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'link']

    def clean(self):
        cleaned_data = super().clean()

        req_title = cleaned_data.get('title')
        req_link = cleaned_data.get('link')

        if Book.objects.filter(title=req_title).exists() or Book.objects.filter(link=req_link).exists():
            raise ValidationError("Book already requested/exists")
