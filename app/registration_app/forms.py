from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    last_name = forms.CharField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name',
                  'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    last_name = forms.CharField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)

    class Meta:
        model = User
        fields = ['username', 'last_name',
                  'first_name', 'email']
