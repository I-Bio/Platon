from Scripts.bottle import redirect
from django.shortcuts import render
from django.views import View

from main.models import StudentGroup, User


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class StudentsList(View):
    def get(self, request, group_pk):
        group = StudentGroup.objects.filter(pk=group_pk)

        if not group.exists():
            return redirect('index')

        return render(request, "students/students_list.html",
                      {'students': User.objects.filter(study_group=group.first())})

    def post(self, request, group_pk):
        ...