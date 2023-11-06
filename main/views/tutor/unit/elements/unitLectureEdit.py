from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from main.forms import TestForm, LectureForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit, Question, Lecture


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
# def unit_lecture_edit_view(request: HttpRequest, unit_id, lecture_id):

class UnitLectureEdit(LoginRequiredMixin, TutorRequiredMixin, View):
    def get(self, request, unit_id, lecture_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        lecture = Lecture.objects.filter(pk=lecture_id)

        if not lecture.exists():
            return redirect('index')

        form = LectureForm(instance=lecture.first())

        return render(request, "content_bank/lecture/edit.html", {'form': form})

    def post(self, request, unit_id, lecture_id):
        lecture = Lecture.objects.filter(pk=lecture_id)
        form = LectureForm(request.POST, instance=lecture.first())

        if not form.is_valid():
            return render(request, "content_bank/lecture/edit.html", {'form': form})

        form.save()

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/lecture/edit.html", {'form': form})