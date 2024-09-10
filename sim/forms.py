from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
    
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

    def save(self,commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['email']  
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_unusable_password()  
        if commit:
            user.save()
        return user        