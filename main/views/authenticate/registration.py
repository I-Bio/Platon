import uuid
from django.db.utils import IntegrityError

from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied, ValidationError

from main.forms import RegistrationForm
from main.models import StudentGroup, User, RegistrationLinks, TutorGroup
from django.contrib.auth.models import Group


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

        return render(request, "auth/registration.html",
                      {'form': RegistrationForm(), 'registration_link': registration_link})

    def post(self, request: HttpRequest, key: str):
        key_uuid = uuid.UUID(key)
        registration_link = RegistrationLinks.objects.get(id=key_uuid)

        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user_group = Group.objects.get(name=form.cleaned_data['group'])

                if TutorGroup.objects.filter(name=user_group):
                    user.is_tutor = True

                group = Group.objects.get(name=user_group)

                user.save()
                user.groups.add(group)
            except IntegrityError:
                error = 'Данная почта уже была зарегистрирована'
                return render(request, "auth/registration.html", {'form': form, 'registration_link': registration_link, 'error': error})

            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            error = 'Проверьте корректность введенных данных'
            return render(request, "auth/registration.html",
                          {'form': form, 'registration_link': registration_link, 'error': error})

        return render(request, "auth/registration.html", {'form': form, 'registration_link': registration_link})
