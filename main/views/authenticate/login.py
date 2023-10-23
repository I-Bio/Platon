from django.shortcuts import render, redirect
from django.http import  HttpRequest
from django.contrib.auth import login, authenticate
from django.views import View

from main.forms import LoginForm


class Login(View):
    def get(self, request: HttpRequest):
        return render(request, "auth/login.html", { 'form': LoginForm() })

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('index')

        return render(request, "auth/login.html", {'form': form})