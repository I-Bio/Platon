from django.shortcuts import render, redirect
from django.views import View

from main.forms import QuestionForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Question


class QuestionEdit(TutorRequiredMixin, View):
    def get(self, request, id):
        question = Question.objects.filter(pk=id)

        if not question.exists():
            return redirect("index")

        form = QuestionForm(instance=question.first())

        return render(request, "content_bank/question/edit.html", {'form': form})

    def post(self, request, id):
        question = Question.objects.filter(pk=id)
        form = QuestionForm(request.POST, instance=question.first())

        if not form.is_valid():
            return render(request, "content_bank/question/edit.html", {'form': form})

        form.save()

        if 'saveAndReturn' in request.POST:
            return redirect('questions_list')

        return render(request, "content_bank/question/edit.html", {'form': form})
