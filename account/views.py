from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, LoginForm

from django.contrib.auth.forms import UserCreationForm
from dashboard.models import Wallet

def registration(request):
	print("hellow")
	print (request.method)
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('dashboard')
	else:
		form = RegistrationForm()

		args = {'form': form}
		return render(request, 'register.html', args)

def registration_view(request):
	context = {}
	print("helre")

	if request.user.is_authenticated:
		return redirect("dashboard")

	if request.POST:
		form = RegistrationForm(request.POST)
		print(form)
		if form.is_valid():
			form.save()
			
			# making wallet model

			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			print(request.user)
			w = Wallet(user = request.user)
			w.save()
			
			return redirect('dashboard')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	print ("here")
	print (context)
	return render(request, 'register.html', context)


def login_view(request):
	context = {}

	user = request.user

	if user.is_authenticated:
		return redirect("dashboard")

	if request.POST:
		form = LoginForm(request.POST)
		print(form)
		print("validity")
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']

			user = authenticate(email=email, password=password)

			if user :
				login(request, user)
				return redirect("dashboard")
	else: form = LoginForm()
	context['login_form'] = form
	return render(request, 'login.html', context)

def logout_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
		
	print("here i am")
	logout(request)
	print ("loggin pout")
	return redirect('home')

