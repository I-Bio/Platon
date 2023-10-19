from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpRequest
from .forms import *
from .models import *

def login_view(request: HttpRequest):

    if request.method != "POST":
        return render(request, "auth/login.html", { 'form': LoginForm() })

    form = LoginForm(request.POST)

    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user is not None:
            login(request, user)
            return redirect('index')
    
    return render(request, "auth/login.html", { 'form': form })

def register(request: HttpRequest):

    if request.method != "POST":
        return render(request, "auth/registration.html", { 'form': RegistrationForm() })

    form = RegistrationForm(request.POST)
        
    if form.is_valid():
        user = User.objects.create_user(
            username = form.cleaned_data['email'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            study_group = StudentGroup.objects.get(name=form.cleaned_data['group']),
            password = form.cleaned_data['password']
        )

        user.save()

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, "auth/registration.html", { 'form': form })
    
    