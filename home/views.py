from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

def home_view(request):
	random_text = "This is home view"

	args = {
		'random_text' : random_text
	}

	return render(request, 'home.html', args)

