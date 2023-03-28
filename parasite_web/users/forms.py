from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True, help_text='Required.')
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', ]