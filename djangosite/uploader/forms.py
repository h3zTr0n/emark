from django import forms

class UploadFileForm(forms.Form):
	Avatar = forms.FileField()