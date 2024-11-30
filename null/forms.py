from django import forms
from .models import ImageFile
from django.contrib.auth.forms import UserCreationForm


class ImageFileForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ['image',]


