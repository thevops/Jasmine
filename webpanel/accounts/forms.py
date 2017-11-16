# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus'}),
                               required=True, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True, label='Password')
