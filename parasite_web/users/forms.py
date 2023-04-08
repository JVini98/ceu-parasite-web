from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#from .models import User

class SignUpForm(UserCreationForm):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            'id': 'first_name',
            'class': 'form-input',
            'name': 'first_name',
            'required': 'true',
            'type': 'text',
            'placeholder': 'Gemma'
        })
        self.fields["last_name"].widget.attrs.update({
            'id': 'last_name',
            'class': 'form-input',
            'name': 'last_name',
            'required': 'true',
            'type': 'text',
            'placeholder': 'Smith'
        })
        self.fields["email"].widget.attrs.update({
            'id': 'email',
            'class': 'form-input',
            'name': 'email',
            'required': 'true',
            'type': 'email',
            'placeholder': 'gemmasmith@mail.com'
        })
        self.fields["password1"].widget.attrs.update({
            'id': 'password1',
            'class': 'form-input',
            'name': 'password1',
            'required': 'true',
            'type': 'password',
            'placeholder': 'Password',
            'minlength': '8',
            'maxlength': '22'
        })
        self.fields["password2"].widget.attrs.update({
            'id': 'password2',
            'class': 'form-input',
            'name': 'password2',
            'required': 'true',
            'type': 'password',
            'placeholder': 'Confirm Password',
            'minlength': '8',
            'maxlength': '22'
        })

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(UserCreationForm):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            'id': 'email',
            'class': 'form-input',
            'name': 'email',
            'required': 'true',
            'type': 'email',
            'placeholder': 'gemmasmith@mail.com'
        })
        self.fields["password1"].widget.attrs.update({
            'id': 'password1',
            'class': 'form-input',
            'name': 'password1',
            'required': 'true',
            'type': 'password',
            'placeholder': 'Password',
            'minlength': '8',
            'maxlength': '22'
        })

    class Meta:
        model = User
        fields = ['email', 'password']

class EmailForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({
            'id': 'email',
            'class': 'form-input',
            'name': 'email',
            'required': 'true',
            'type': 'email',
            'placeholder': 'gemmasmith@mail.com'
        })
    class Meta:
        model = User
        fields = ['email']