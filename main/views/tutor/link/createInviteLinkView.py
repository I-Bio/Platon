from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

from main.forms import CreateInviteLinkForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import RegistrationLinks


class CreateInviteLinkView(TutorRequiredMixin, View):
    def get(self, request):
        form = CreateInviteLinkForm(is_staff=request.user.is_staff)
        return render(request, template_name="tutor/createInviteLink.html", context={'form': form})

    def post(self, request):
        form = CreateInviteLinkForm(request.POST, is_staff=request.user.is_staff)

        if not form.is_valid():
            return render(request, template_name="tutor/createInviteLink.html")

        form.save()

        group_name = form.cleaned_data['group_name']
        registration_link_id = RegistrationLinks.objects.get(group_name=group_name).id

        registration_link = request.build_absolute_uri(reverse('registration', kwargs={'key': registration_link_id}))

        print(registration_link)

        return render(request, template_name="tutor/createInviteLink.html",
                      context={'form': form, 'registration_link': registration_link})
