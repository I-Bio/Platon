from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import UserTask, Task, StudentGroup, User


class StudentsWorkList(TutorRequiredMixin, View):
    def get(self, request, task_id, group_id):
        users_task_info = UserTask.objects.filter(group_id=group_id, main_task_id=task_id)
        name_main_task_info = Task.objects.filter(id=task_id).first()
        name_groups = StudentGroup.objects.all()
        name_group = StudentGroup.objects.filter(id=group_id).first()

        user_info = User.objects.filter(groups=group_id)

        user_id_list = []
        for i in users_task_info:
            user_id_list.append(i.user_id.pk)

        context = {
            'name_main_task_info' : name_main_task_info,
            'name_groups' : name_groups,
            'name_group' : name_group,
            'user_info' : user_info,
            'user_id_list' : user_id_list,
        }
        return render(request, 'students/StudentsTaskList/studentsWork.html', context=context)

