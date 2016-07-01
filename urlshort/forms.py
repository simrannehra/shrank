from django import forms
from django.contrib.auth.models import User
from .models import Sam

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model =User
		fields=['username','email','password']

class loginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model =User
		fields=['username','password']

class addurl(forms.ModelForm):
	class Meta:
		model = Sam
		fields = [
			"originalurl",
			"shorten"
		]