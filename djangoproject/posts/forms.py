from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(forms.Form):
	email = forms.EmailField(max_length = 100, widget=forms.EmailInput(
		attrs={
		"id": "icon_prefix",
		"class": "validate",
		}))
	password = forms.CharField(max_length = 100, widget=forms.PasswordInput(
		attrs={
		"id": "icon_prefix",
		"class": "validate",
		}))

class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(
		attrs={
		"id": "icon_prefix username",
		"class": "validate",
		}))
	email = forms.EmailField(widget=forms.EmailInput(
		attrs={
		"id": "icon_prefix email",
		"class": "validate",
		}))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
		"id": "icon_prefix password",
		"class": "validate",
		}))
	password2 =forms.CharField(widget=forms.PasswordInput(
		attrs={
		"id": "icon_prefix password2",
		"class": "validate",
		}))
	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username is taken")
		return username
	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("Email is taken")
		return email
	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Password must match.")
		return data