import uuid
from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied

from main.forms import RegistrationForm
from main.models import StudentGroup, User, RegistrationLinks


class Registration(View):
    def get(self, request: HttpRequest, key: str):
        try:
            key_uuid = uuid.UUID(key)
            registration_link = RegistrationLinks.objects.get(id=key_uuid)
        except (ValueError, RegistrationLinks.DoesNotExist):
            raise Http404

        if registration_link.end_date < timezone.now():
            registration_link.delete()
            raise PermissionDenied()

        return render(request, "auth/registration.html", {'form': RegistrationForm()})

    def post(self, request: HttpRequest):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                study_group=StudentGroup.objects.get(name=form.cleaned_data['group']),
                password=form.cleaned_data['password']
            )

            user.save()

            if user is not None:
                login(request, user)
                return redirect('index')

        return render(request, "auth/registration.html", {'form': form})
