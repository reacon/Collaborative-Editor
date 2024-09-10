from .models import Documents
from django import forms

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['name','content']
