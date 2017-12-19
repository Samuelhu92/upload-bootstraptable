from django import forms
from .utils import validate_excel_file


class UploadFileForm(forms.Form):
    file_filed = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), validators=[validate_excel_file])

