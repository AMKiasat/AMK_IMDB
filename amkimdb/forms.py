from django import forms


class UploadFileForm(forms.Form):
    username = forms.CharField(max_length=50)
    file = forms.FileField(label='voice')
