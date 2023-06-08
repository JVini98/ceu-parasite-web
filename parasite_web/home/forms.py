from django import forms
from .models import Name
from users.forms import PasswordForm

class NameForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'first_name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'last_name'
        })
    )

    class Meta:
        model = Name
        fields = ['first_name', 'last_name']

class PasswordFormStyle(PasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
