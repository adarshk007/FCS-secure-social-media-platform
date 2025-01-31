from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import Account

class EditProfileForm(UserChangeForm):

	class Meta:
		model = Account
		fields = (
			'email',
			'first_name',
			'last_name',
			'phone_no'
		)

