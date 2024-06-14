from django import forms

class PdfUploadForm(forms.Form):
    email = forms.EmailField(required=True)
    file = forms.FileField(required=True)
