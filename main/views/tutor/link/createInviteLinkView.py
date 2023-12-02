from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

from main.forms import CreateInviteLinkForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import RegistrationLinks


class CreateInviteLinkView(TutorRequiredMixin, View):
    def get(self, request):
        is_staff = request.user.is_staff
        is_tutor = request.user.is_tutor
        form = CreateInviteLinkForm(is_staff=is_staff, is_tutor=is_tutor)
        return render(request, template_name="tutor/createInviteLink.html", context={'form': form, 'is_staff': is_staff, 'is_tutor': is_tutor})

    def post(self, request):
        is_staff = request.user.is_staff
        is_tutor = request.user.is_tutor
        form = CreateInviteLinkForm(request.POST, is_staff=is_staff, is_tutor=is_tutor)

        if not form.is_valid():
            return render(request, template_name="tutor/createInviteLink.html", context={'form': form, 'is_staff': is_staff, 'is_tutor': is_tutor})

        form.save()

        group_name = form.cleaned_data['group_name']
        registration_link_id = RegistrationLinks.objects.get(group_name=group_name).id

        registration_link = request.build_absolute_uri(reverse('registration', kwargs={'key': registration_link_id}))

        return render(request, template_name="tutor/createInviteLink.html",
                      context={'form': form, 'is_staff': is_staff, 'is_tutor': is_tutor, 'registration_link': registration_link})
