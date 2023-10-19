from django.shortcuts import render, redirect
from django.views import View

from main.forms import QuestionForm
from main.models import Question


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class QuestionEdit(View):
    def get(self, request):
        question = Question.objects.filter(pk=id)

        if not question.exists():
            return render('index')

        form = QuestionForm(instance=question.first())

        return render(request, "content_bank/question/edit.html", {'form': form})

    def post(self, request):
        question = Question.objects.filter(pk=id)
        form = QuestionForm(request.POST, instance=question.first())

        if not form.is_valid():
            return render(request, "content_bank/question/edit.html", {'form': form})

        form.save()

        if 'saveAndReturn' in request.POST:
            return redirect('questions_list')

        return render(request, "content_bank/question/edit.html", {'form': form})
