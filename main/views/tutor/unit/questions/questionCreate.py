from django.shortcuts import render, redirect
from django.views import View

from main.forms import QuestionForm
from main.mixins.tutorRequired import TutorRequiredMixin


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class QuestionCreate(TutorRequiredMixin, View):
    def get(self, request):
        return render(request, "content_bank/question/edit.html", {'form': QuestionForm()})

    def post(self, request):
        form = QuestionForm(request.POST)

        if not form.is_valid():
            return render(request, "content_bank/question/edit.html", {'form': form})

        form.save()

        if 'saveAndReturn' in request.POST:
            return redirect('questions_list')

        return redirect('question_edit', form.instance.pk)