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

        print("JIB<RF")
        group_check_info = GroupCheck.objects.filter(usser_id=who_check, main_task_id=main_task_id)

        flag = False
        if group_check_info[0]:
            for list_user in group_check_info[0].user_check_id:
                if list_user == user_id:
                    flag = True
        else:
            return HttpResponse('Вас не назначили на проверку этого задания этой группы')

        if flag != True:
            return HttpResponse('Вас не назначили проверять этого человека')

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

                return redirect('select_student.html', user_id=user_id, main_task_id=main_task_id, who_check=who_check )
        else:
            form = UserTask()
        return render(request, 'students/checkTask/grade_group.html', {'form': form})

