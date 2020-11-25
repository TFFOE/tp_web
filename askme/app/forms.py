from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Логин', min_length=4, max_length=30, required=True)
    password = forms.CharField(label = 'Пароль', min_length=3, max_length=16, required=True)