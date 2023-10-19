from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from main.models import StudentGroup


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class GroupsList(View):
    def get(self, request: HttpRequest):
        return render(request, "students/groups_list.html", {'groups': StudentGroup.objects.all()})

    def post(self, request: HttpRequest):
        ...
