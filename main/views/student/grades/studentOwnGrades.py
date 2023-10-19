from django.shortcuts import render
from django.views import View


# @login_required(login_url='/login/', redirect_field_name=None)
class StudentOwnGrades(View):
    def get(self, request):
        return render(request, "students/own_grades.html", request.user.get_grades() | {'student': request.user})

    def post(self, request):
        ...