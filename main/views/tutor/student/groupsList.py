from django.contrib.auth.models import Group
from django.http import HttpRequest, Http404
from django.shortcuts import render
from django.views import View

from main.forms import IdSelector
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import StudentGroup, Subject, User


class GroupsList(TutorRequiredMixin, View):

    def get(self, request):
        return self.init(request, self.doGet)

    def post(self, request):
        return self.init(request, self.doPost)

    def init(self, request, action):
        form = IdSelector(request.POST)
        subjects = Subject.objects.filter(tutor_id=request.user.pk)
        subject_selected = None
        groups = None
        return action(request, form, subjects, subject_selected, groups)

    def doGet(self, request, form, subjects, subject_selected, groups):
        if subjects.exists() == True:
            subject_selected = subjects.first()
            groups = Group.objects.filter(id__in=subject_selected.enrolled_groups_id)

        return self.responseData(request, form, subjects, subject_selected, groups)

    def doPost(self, request, form, subjects, subject_selected, groups):
        if form.is_valid():
            subject = form.cleaned_data['id']
            subject_selected = subjects.filter(id=subject).first()
            groups = Group.objects.filter(id__in=subject_selected.enrolled_groups_id)

        return self.responseData(request, form, subjects, subject_selected, groups)

    def responseData(self, request, form, subjects, subject_selected, groups):
        return render(request, template_name="students/groups_list.html",
                      context={
                          'form': form,
                          'subjects': subjects,
                          'groups': groups,
                          'subject_selected_object': subject_selected,
                      })
