from django import forms
from .models import Name

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
