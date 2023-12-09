import json

from django.shortcuts import render, redirect
from django.views import View

from main.forms import AdderToTheCourceForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Subject, StudentGroup, User


class AdderToTheCourseView(TutorRequiredMixin, View):
    def get(self, request):
        try:
            subjects = Subject.objects.filter(tutor_id=request.user.pk)
            enrolled_groups_id = subjects[0].enrolled_groups_id
            enrolled_groups = StudentGroup.objects.filter(name__in=enrolled_groups_id)
            not_enrolled_groups = StudentGroup.objects.exclude(name__in=enrolled_groups_id)
        except IndexError:
            subjects = []
            enrolled_groups = []
            not_enrolled_groups = []

        return render(request, template_name="tutor/addingToTheCourse.html",
                      context={'form': AdderToTheCourceForm, 'subjects': subjects, 'enrolled_groups': enrolled_groups,
                               'not_enrolled_groups': not_enrolled_groups})

    def post(self, request):
        subjects = Subject.objects.filter(tutor_id=request.user.pk)

        form = AdderToTheCourceForm(request.POST)

        if not form.is_valid():
            return redirect('add_to_the_cource')

        subjects_of_this_teacher = form.cleaned_data['subjects_of_this_teacher']

        if "submitButton" in request.POST:
            enrolled_student_group_values = request.POST.getlist('student_group')
            enrolled_student_group_values = list(map(int, enrolled_student_group_values))

            form.save(enrolled_student_group_values)

            enrolled_group_names = subjects.get(pk=subjects_of_this_teacher).enrolled_groups_id
            enrolled_groups = StudentGroup.objects.filter(name__in=enrolled_group_names)
            not_enrolled_groups = StudentGroup.objects.exclude(name__in=enrolled_group_names)

            return render(request, template_name="tutor/addingToTheCourse.html",
                          context={'form': AdderToTheCourceForm, 'subjects': subjects,
                                   'enrolled_groups': enrolled_groups,
                                   'not_enrolled_groups': not_enrolled_groups,
                                   'subjects_of_this_teacher': subjects_of_this_teacher})

        if "subjects_of_this_teacher" in request.POST:
            enrolled_group_names = subjects.get(pk=subjects_of_this_teacher).enrolled_groups_id
            enrolled_groups = StudentGroup.objects.filter(name__in=enrolled_group_names)
            not_enrolled_groups = StudentGroup.objects.exclude(name__in=enrolled_group_names)

            return render(request, template_name="tutor/addingToTheCourse.html",
                          context={'form': AdderToTheCourceForm, 'subjects': subjects,
                                   'enrolled_groups': enrolled_groups,
                                   'not_enrolled_groups': not_enrolled_groups,
                                   'subjects_of_this_teacher': subjects_of_this_teacher})
