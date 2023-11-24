from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from main.forms import ChooseStudentsToChecker
from main.models import GroupCheck, User, Task, StudentGroup, UserTask


class AssignStudent(View):
    def get(self, request, user_id, main_task_id):
        info_task_user = UserTask.objects.filter(user_id=user_id).first()
        user_name = User.objects.filter(id=info_task_user.pk).first()

        info_user = User.objects.filter(groups__name=info_task_user.group_id)

        info_user_id_list = GroupCheck.objects.filter(usser_id=user_id).first().user_check_id
        filet_users = User.objects.filter(id__in=info_user_id_list)

        sasy = info_user.exclude(id__in=filet_users)


        context = {
            'user_name' : user_name,
            'filet_users' : filet_users,
            'info_task_user' : info_task_user,

            'user_id' : user_id,
            'main_task_id': main_task_id,
            'sasy' : sasy,

        }
        return render(request, 'students/checkTask/select_student.html', context=context)
    def post(self, request, user_id, main_task_id):
        list_checker_student = request.POST.getlist('questions[]')

        if GroupCheck.objects.filter(usser_id=user_id).first():
            a = GroupCheck.objects.filter(usser_id=user_id).first()
            a.user_check_id = [int(i) for i in list_checker_student ]
        else:
            a = GroupCheck(usser_id=user_id, main_task_id=main_task_id, user_check_id=list_checker_student)
        a.save()

        form = ChooseStudentsToChecker(request.POST)

        if form.is_valid() == True:
            context = {
                'form': form,
                'questions': GroupCheck.objects.all(),

                'user_id': user_id,
                'main_task_id': main_task_id,
            }

            return render(request, "students/checkTask/select_student.html", context=context)

        return redirect('select_students', user_id=user_id, main_task_id=main_task_id)
