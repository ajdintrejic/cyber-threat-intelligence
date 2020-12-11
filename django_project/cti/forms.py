from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

class AddressForm(forms.Form):
    address = forms.CharField(label='Address')
