from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from main.models import Subject


# @login_required(login_url='/login/', redirect_field_name=None)
class Index(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = None

    def get(self, request):
        if request.user.is_staff or request.user.is_tutor:
            subjects = Subject.objects.filter(tutor_id=request.user).order_by('name')
        else:
            group_user = request.user.groups.first().pk
            subjects_all = Subject.objects.all().order_by('name')
            subjects = []
            for subject in subjects_all:
                if group_user in subject.enrolled_groups_id:
                    subjects.append(subject)

        return render(request, "index.html", {'subjects': subjects})

    def post(self, request):
        ...