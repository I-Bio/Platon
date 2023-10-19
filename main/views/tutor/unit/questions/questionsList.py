from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from main.models import Question


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class QuestionsList(View):
    def get(self, request):
        return render(request, "content_bank/question/list.html", {'questions': Question.objects.all()})

    def post(self, request):
        if 'toDelete' in request.POST:

            question = Question.objects.filter(pk=int(request.POST['toDelete']))

            if not question.exists():
                return HttpResponse()

            question.first().delete()

            return HttpResponse()

        return render(request, "content_bank/question/list.html", {'questions': Question.objects.all()})

