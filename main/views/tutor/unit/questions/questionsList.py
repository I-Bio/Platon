from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Question, Subject


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class QuestionsList(TutorRequiredMixin, View):
    def get(self, request):
        subjects_of_this_teacher = Subject.objects.filter(tutor_id=request.user.id).first()
        return render(request, "content_bank/question/list.html",
                      {'questions': Question.objects.filter(question_creator=request.user, question_subject=subjects_of_this_teacher)})

    def post(self, request):
        if 'toDelete' in request.POST:

            question = Question.objects.filter(pk=int(request.POST['toDelete']), question_creator_id=request.user.pk)

            if not question.exists():
                return HttpResponse()

            question.first().delete()

            return HttpResponse()

        if 'subjects_of_this_teacher' in request.POST:
            subjects_of_this_teacher_id = int(request.POST['subjects_of_this_teacher'])
            subjects_of_this_teacher = Subject.objects.get(pk=subjects_of_this_teacher_id)
            questions = Question.objects.filter(question_creator=request.user,
                                                question_subject=subjects_of_this_teacher)

            return render(request, "content_bank/question/list.html",
                          {'questions': questions, 'subjects_of_this_teacher': subjects_of_this_teacher})




        return render(request, "content_bank/question/list.html",
                      {'questions': Question.objects.filter(question_creator=request.user)})
