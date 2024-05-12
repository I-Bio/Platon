
from django.views import View
from django.shortcuts import redirect, render

from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from main.models import Subject, Question, Test




class TestPreparation(View, StudentGroupRequiredMixin):
    def get(self, request):
        subjects = Subject.objects.all()
        list_subject_user = []

        for subject in subjects:
            if request.user.groups.first().pk in subject.enrolled_groups_id:
                list_subject_user.append(subject)

        list_quastions = []
        quastions = Question.objects.filter(question_subject_id__in = list_subject_user)
        for quastion in quastions:
            list_quastions.append(quastion)

        test_user = Test.objects.filter(name=str(request.user)).first()
        if Test.objects.filter(name=str(request.user)):
            test_user.questions.set(list_quastions)
        else:
            test_user = Test(
                name=str(request.user),
                description=f"Госэкзамен студента {request.user.first_name} {request.user.last_name}",
                start_date="2000-01-01 00:00:00",
                end_date="2100-01-01 00:00:00",
            )
            test_user.save()
            test_user.questions.set(list_quastions)
        return render(request, "students/testStatePreparation.html")
    def post (self, request):
        if request.POST:
            return redirect('test_state')