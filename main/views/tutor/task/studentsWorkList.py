from django.shortcuts import render
from django.views import View
from django.http import Http404
from django.contrib.auth.models import Group

from main.forms import GroupSelector
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import UserTask, Task, StudentGroup, User, Subject


class StudentsWorkList(TutorRequiredMixin, View):
    def get(self, request, subject_id, task_id):
        return self.init(request, subject_id, task_id, self.doGet)

    def post(self, request, subject_id, task_id):
        return self.init(request, subject_id, task_id, self.doPost)

    def init(self, request, subject_id, task_id, action):
        subject = Subject.objects.get(id=subject_id)

        if subject == None or len(subject.enrolled_groups_id) <= 0:
            raise Http404()

        task = Task.objects.get(id=task_id)

        if task == None:
            raise Http404()

        groups = StudentGroup.objects.filter(name__in=subject.enrolled_groups_id)
        
        return action(request, subject_id, groups, task)

    def doGet(self, request, subject_id, groups, task):
        selected_group = groups.first()
        return self.responseData(request, subject_id, task, groups, selected_group)

    def doPost(self, request, subject_id, groups, task):
        form = GroupSelector(request.POST)
        selected_group = None
        if form.is_valid():
            selected_group = groups.get(id=form.cleaned_data['group'])

        return self.responseData(request, subject_id, task, groups, selected_group)

    def responseData(self, request, subject_id, task, groups, selected_group):
        userData = self.createUserDataObject(selected_group.pk, task.pk) if selected_group != None else None
        data = {
            'groups': groups,
            'userData': userData,
            'requestData': {
                "task": task,
                "subject_id": subject_id,
            },
            'selected_group': selected_group,
        }

        return render(request, 'students/StudentsTaskList/studentsWork.html', context=data)

    def createUserDataObject(self, group_id, task_id):
        userTasks = UserTask.objects.filter(group_id=group_id, main_task_id=task_id)
        users = StudentGroup.objects.get(id=group_id).name.user_set.all()
        users_complete_list = []

        for userTask in userTasks:
            users_complete_list.append(userTask.user_id.pk)

        result = {
            "users": users,
            "users_complete_list": users_complete_list,
        }

        return result
