from django import forms
from .models import *
from django.forms import CheckboxSelectMultiple, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class RegisterUserForm(UserCreationForm):
	username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'placeholder':'Логин'
		}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'placeholder':'Электронная почта'
		}))

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Пароль'
		}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Подтверждение пароля'
		}))

	class Meta:
		model = User
		fields = ("username","email","password1","password2")

class TravelInfoForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(label='Phone', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    age = forms.IntegerField(label='Age', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    passport_no = forms.CharField(label='Passport Number', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    nationality = forms.CharField(label='Nationality', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    sex = forms.CharField(label='Sex', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
