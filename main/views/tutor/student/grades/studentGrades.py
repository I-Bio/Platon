from django.shortcuts import redirect, render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import User


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class StudentGrades(TutorRequiredMixin, View):
    def get(self, request, student_pk):
        student = User.objects.filter(pk=student_pk)

        if not student.exists():
            return redirect('index')

        student = student.first()

        return render(request, "students/student_grades.html", student.get_grades() | {'student': student})

    def post(self, request, student_pk):
        ...