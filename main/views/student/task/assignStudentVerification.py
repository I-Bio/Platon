from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from main.forms import ChooseStudentsToChecker
from main.models import GroupCheck, User, Task, StudentGroup, UserTask


class AssignStudent(View):
    def get(self, request, user_id, main_task_id):
        return self.init(request, user_id, main_task_id, self.doGet)

    def post(self, request, user_id, main_task_id):
        return self.init(request, user_id, main_task_id, self.doPost)

    def init(self, request, user_id, main_task_id, action):
        userTasks = UserTask.objects.filter(user_id=user_id)

        if userTasks.exists() == False:
            raise Http404
        else:
            userTask = userTasks.first()

        user = User.objects.get(id=userTask.pk)

        return action(request, user_id, main_task_id, user, userTask)

    def doGet(self, request, user_id, main_task_id, user, userTask):
        groupCheck = GroupCheck.objects.filter(usser_id=user_id).first()
        return self.responseData(request, user_id, main_task_id, user, userTask, groupCheck)

    def doPost(self, request, user_id, main_task_id, user, userTask):
        form = ChooseStudentsToChecker(request.POST)

        if form.is_valid() == False:
            return HttpResponse("Форма не прошла проверку")

        form.clean()
        selectedStudents = form.cleaned_data["idList[]"]
        groupCheck = GroupCheck.objects.filter(usser_id=user_id).first()

        if groupCheck != None:
            groupCheck.user_check_id = selectedStudents
        else:
            groupCheck = GroupCheck(usser_id=user_id, main_task_id=main_task_id, user_check_id=selectedStudents)

        groupCheck.save()
        return self.responseData(request, user_id, main_task_id, user, userTask, groupCheck)

    def responseData(self, request, user_id, main_task_id, user, userTask, groupCheck):
        selectedUsers, unselectedUsers = self.collectUsers(userTask, groupCheck)
        data = {
            'user': user,
            'selectedUsers': selectedUsers,

            'user_id': user_id,
            'main_task_id': main_task_id,
            'unselectedUsers': unselectedUsers,
        }
        return render(request, 'students/checkTask/select_student.html', context=data)

    def collectUsers(self, userTask, groupCheck):
        selectedUsers = None

        if groupCheck != None:
            selectedUsers = User.objects.filter(id__in=groupCheck.user_check_id)
            unselectedUsers = selectedUsers.exclude(id__in=selectedUsers)
        else:
            unselectedUsers = User.objects.filter(groups__name=userTask.group_id)

        return selectedUsers, unselectedUsers