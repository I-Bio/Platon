from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from main.forms import QuestionForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Question
from main.views.MessageSuccess import MessageSuccess


class QuestionEdit(TutorRequiredMixin, View, MessageSuccess):
    def get(self, request, id):
        question = Question.objects.filter(pk=id)

        if not question.exists():
            return redirect("index")

        form = QuestionForm(instance=question.first(), question_creator_id=request.user.pk)

        return render(request, "content_bank/question/edit.html", {'form': form, 'question_subject': question.first().question_subject})

    def post(self, request, id):
        question = Question.objects.filter(pk=id)
        form = QuestionForm(request.POST, instance=question.first(), question_creator_id=request.user.pk)

        if not form.is_valid():
            return render(request, "content_bank/question/edit.html", {'form': form, 'question_subject': question.first().question_subject})

        form.save()

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            return redirect('questions_list')

        return render(request, "content_bank/question/edit.html", {'form': form, 'question_subject': question.first().question_subject})
