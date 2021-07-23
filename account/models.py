from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, first_name, last_name, phone_no, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username: 
			raise ValueError("User must have a username")
		if not first_name: 
			raise ValueError("User must have a first name")
		if not last_name: 
			raise ValueError("User must have a last name")
		if not phone_no: 
			raise ValueError("User must have a phone number")

		user = self.model(
				email=self.normalize_email(email),
				username=username,
				first_name=first_name,
				last_name=last_name,
				phone_no=phone_no,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, last_name, phone_no, password):
		user = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
				first_name=first_name,
				last_name=last_name,
				phone_no=phone_no,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(verbose_name="username", max_length=30, unique=True)
	first_name = models.CharField(verbose_name="first name", max_length=30)
	last_name = models.CharField(verbose_name="last name", max_length=30)
	phone_no = models.CharField(verbose_name="phone number", max_length=10, unique=True)
	date_joined = models.DateTimeField(verbose_name="data joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_casual_user = models.BooleanField(default=True)
	is_premium_user = models.BooleanField(default=False)
	is_commercial_user = models.BooleanField(default=False)
	is_verified = models.BooleanField(default=False)
	premium_type = models.IntegerField(default=0, verbose_name="premium_type")

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_no']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
