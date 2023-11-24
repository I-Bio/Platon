from django.shortcuts import render
from django.views import View

from main.models import StudentGroup, Task, UserTask, User


class showUncompletedTasks(View):
    def get(self, request, task_id, group_id):
        name_groups = StudentGroup.objects.all()
        name_main_task_info = Task.objects.filter(id=task_id)[0]
        name_group = StudentGroup.objects.filter(id=group_id)[0]
        print(name_main_task_info)
        user_task_info = UserTask.objects.filter(group_id=group_id, main_task_id=task_id)
        user_info = User.objects.filter(groups=group_id)


        arr_completed_task_user_id = []
        for user_task in user_task_info:
            arr_completed_task_user_id.append(user_task.user_id.pk)

        print(user_info, arr_completed_task_user_id)

        for stud in user_info:
            if stud.pk in arr_completed_task_user_id:
                print(stud.last_name, stud.pk, 'выполнил')
            else:
                print(stud.last_name, stud.pk, 'не выполнил')

        context = {
            'task_id' : task_id,
            'group_id' : group_id,

            'name_groups' : name_groups,
            'name_main_task_info' : name_main_task_info,
            'user_info' : user_info,
            'name_group' : name_group,
            'arr_completed_task_user_id' : arr_completed_task_user_id,
        }
        return render(request, 'tutor/tasks_to_be_checked.html', context=context)