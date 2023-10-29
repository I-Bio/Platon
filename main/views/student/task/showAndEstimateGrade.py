from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from main.forms import UserTaskForm
from main.models import UserTask, User, Task, GroupCheck, StudentGroup


class GradeTask(View):
    def get(self, request, user_id, main_task_id, who_check):
        form = UserTaskForm()
        task_info = UserTask.objects.filter(main_task_id=main_task_id, user_id=user_id)
        task_name = Task.objects.filter(id=main_task_id)
        info_group_check = GroupCheck.objects.filter(usser_id=who_check)

        info_group_id = StudentGroup.objects.filter(name=task_info[0].group_id)

        # print(info_group_check[0].group_check, info_group_id[0].id)

        try:
            flag = False
            if info_group_check[0].group_check == info_group_id[0].id:
                for user_check in info_group_check:
                    if user_check.usser_id == who_check:
                        flag = True
        except:
            return HttpResponse('У вас нет доступа или нет такого задания')
        if flag == False:
            return HttpResponse('У вас нет доступа')

        context = {
            'form' : form,
            'task_info' : task_info[0],
            'task_name' : task_name[0],

            'who_check' : who_check,
            'user_id' : user_id,
            'main_task_id' : main_task_id,
        }



        return render(request, 'students/checkTask/grade_group.html', context=context)

    def post(self, request, user_id, main_task_id, who_check):
        if request.method == "POST":
            form = UserTaskForm(request.POST)
            if form.is_valid():
                selected_grade = form.cleaned_data['grade']
                user_task = UserTask.objects.get(user_id=user_id, main_task_id=main_task_id)
                user_task.grade = selected_grade
                user_task.save()

                return redirect('grade_group', user_id=user_id, main_task_id=main_task_id, who_check=who_check )
        else:
            form = UserTask()
        return render(request, 'students/checkTask/grade_group.html', {'form': form})

