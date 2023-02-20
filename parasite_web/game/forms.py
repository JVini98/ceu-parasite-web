from django import forms
from .models import CroppedImage

class CroppedImageForm(forms.ModelForm):
    class Meta:
        model = CroppedImage
        fields = ('file', )