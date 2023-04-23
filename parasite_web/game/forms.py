from django import forms

class ReportPhotographForm(forms.Form):
    image_reported = forms.CharField(widget=forms.HiddenInput())