from django.shortcuts import render, redirect
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import StudentGroup, User


class StudentsList(TutorRequiredMixin, View):
    def get(self, request, group_pk):


        group = StudentGroup.objects.filter(pk=group_pk)

        print(User.objects.filter(groups=group[0].pk))

        if not group.exists():
            return redirect('index')


        return render(request, "students/students_list.html",
                      {'students': User.objects.filter(groups=group[0].pk)})

    def post(self, request, group_pk):
        ...