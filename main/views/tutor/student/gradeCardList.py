from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import StudentGroup, Subject


class ShowGradeCardList(TutorRequiredMixin, View):
    def get(self, request, group_id, subject_id):
        info_group = StudentGroup.objects.filter(id=group_id).first().name
        info_subject = Subject.objects.filter(id=subject_id).first()
        print(info_subject.name)
        context = {
        'info_group_name' : info_group,
        'info_subject' : info_subject,


        }
        return render(request, 'tutor/grade_card.html', context=context)