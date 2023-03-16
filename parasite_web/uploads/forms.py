from django import forms
from django.utils.safestring import mark_safe

from .models import ParasiteImage


class ParasiteImageForm(forms.ModelForm):
    class Meta:
        model = ParasiteImage
        fields = ['path']
        labels = {
            "path": ""
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['image'].label = mark_safe('Upload Image<br>')

