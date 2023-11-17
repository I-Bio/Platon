from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin


class ShowGradeCardList(TutorRequiredMixin, View):
    def get(self, request, group_id, subject_id):
        return HttpResponse("asasasa")
        # return  render(request, 'tutor/grade_card.html')