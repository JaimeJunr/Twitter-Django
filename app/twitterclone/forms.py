# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import (
    User,
    Comment,
)  # Certifique-se de que este é o caminho correto para o seu modelo personalizado
from django.core.exceptions import ValidationError
from django.db import models


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Crie uma senha"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirme sua senha"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Seu Nome de Usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Seu Email"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite seu nome de usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image"]  # Este campo deve estar presente no seu modelo personalizado

class CoverImageForm(forms.ModelForm): # Adicionado o formulario CoverImageForm
    class Meta:
        model = User
        fields = ['cover_image']

    
class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio'] # adicionado os campos first_name e last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.instance.username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este username já está em uso.')
        return username
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # Apenas o campo de conteúdo do comentário
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Escreva um comentário...",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
        }


class TweetForm(forms.Form):
    content = forms.CharField(max_length=280, widget=forms.Textarea(attrs={'id': 'tweetContent'}))