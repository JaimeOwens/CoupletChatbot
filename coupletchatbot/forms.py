from django import forms
from django.forms.formsets import MAX_NUM_FORM_COUNT

class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=48, widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder':'Email'}))
    password = forms.CharField(label='password', max_length=16, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'Password'}))

class RegisterForm(forms.Form):
    email = forms.EmailField(label='email', max_length=48, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Email'}))
    username = forms.CharField(label='username', max_length=16, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder':'Username'}))
    password1 = forms.CharField(label='password', max_length=16, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'Password'}))
    password2 = forms.CharField(label='comfirm_password', max_length=16, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder':'Password'}))