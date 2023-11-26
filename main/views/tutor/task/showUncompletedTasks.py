from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View

from main.models import StudentGroup, Task, UserTask, User, GroupCheck


class showUncompletedTasks(View):
    def get(self, request, main_task_id):

        group_obj = GroupCheck.objects.filter(user_id=request.user.pk).first()

        if group_obj == None:
            raise PermissionDenied()

        main_task_id = group_obj.main_task_id.pk

        group_check = GroupCheck.objects.filter(usser_id=request.user.pk)

        if group_check.count() == 0:
            raise PermissionDenied()

        group_check_all = group_check.all()

        arr_name_tasks = []
        for name_task in group_check_all:
            arr_name_tasks.append(name_task.main_task_id)


        group_check = group_check.filter(main_task_id=main_task_id)
        if group_check.count() == 0:
            raise PermissionDenied()

        name_group = request.user.groups.all().first()
        name_task = group_check.first().main_task_id

        list_whom_can_check = group_check.first().user_check_id
        user_info = User.objects.filter(groups=request.user.groups.all().first(), id__in=list_whom_can_check)


        task_user = UserTask.objects.filter(group_id=request.user.groups.all().first().pk, main_task_id=main_task_id)
        list_checked = []
        for task in task_user:
            list_checked.append(task.user_id.pk)



        context = {
            'arr_name_tasks' : arr_name_tasks,
            'user_info' : user_info,
            'name_group' : name_group,
            'name_task' : name_task,
            'list_checked' : list_checked,

            'main_task_id' : main_task_id,
        }
        return render(request, 'tutor/tasks_to_be_checked.html', context=context)