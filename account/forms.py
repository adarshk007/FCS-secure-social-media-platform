from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True, max_length=60, help_text='Required. Add a valid email address')

	class Meta:
		model = Account
		fields = (
			'username', 
			'first_name', 
			'last_name', 
			'email', 
			'password1', 
			'password2',  
			'phone_no',
		)
	
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['username']
		user.phone_no = self.cleaned_data['phone_no']
		

		if commit:
			user.save()

		return user


class LoginForm(forms.ModelForm):
	# username = forms.CharField(max_length=254)
	password = forms.CharField(label=("Password"), widget=forms.PasswordInput)
	class Meta:
		model = Account
		fields = (
			'email', 
			'password'
		)

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")
