from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from main.models import User, TestResult


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class StudentGradeChanger(View):
    def get(self, request, student_pk, grade_pk):
        student = User.objects.filter(pk=student_pk)

        if not student.exists():
            return redirect('index')

        result = TestResult.objects.filter(pk=grade_pk)

        if not result.exists():
            return redirect('index')

        result = result.first()

        return render(request, "students/change_grade.html", {'result': result})

    def post(self, request, student_pk, grade_pk):
        student = User.objects.filter(pk=student_pk).first()
        result = TestResult.objects.filter(pk=grade_pk).first()

        if not 'score' in request.POST:
            return HttpResponse(status=400)

        score = int(request.POST['score'])

        if score < 0 or score > 100:
            return HttpResponse(status=400)

        result.set_result_from_score(score)
        result.save()

        if 'saveAndReturn' in request.POST:
            return redirect('student_grades', student.pk)

        return render(request, "students/change_grade.html", {'result': result})
