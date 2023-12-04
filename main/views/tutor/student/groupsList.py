from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from main.forms import SelectSubjet
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import StudentGroup, Subject, User


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class GroupsList(TutorRequiredMixin, View):

    def get(self, request):
        subjects = Subject.objects.filter(tutor_id=request.user.pk)
        form = SelectSubjet(request.POST)


        return render(request, template_name="students/groups_list.html",
                      context={
                          'groups': Group.objects.filter(id__in=subjects.all().first().enrolled_groups_id)
,
                          'subjects': subjects,
                          'form' : form,})

    def post(self, request):
            subjects = Subject.objects.filter(tutor_id=request.user.pk)
            form = SelectSubjet(request.POST)

            subject_selected_object = None
            if form.is_valid():
                subject_selected = form.cleaned_data['subject']

                subject_selected_object = subjects.filter(id=subject_selected).first()
                groups = Group.objects.filter(id__in=subjects.filter(id=subject_selected).first().enrolled_groups_id)






            return render(request, template_name="students/groups_list.html",
                          context={
                              'subjects': subjects,
                              'form' : form,
                              'groups' : groups,

                              'subject_selected_object' : subject_selected_object,
                          }
                          )
