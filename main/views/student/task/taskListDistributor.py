from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View

from main.forms import IdSelector
from main.models import StudentGroup, Task, UserTask, User, GroupCheck


class TaskListDistributor(View):
    def get(self, request):
        return self.init(request, self.doGet)

    def post(self, request):
        return self.init(request, self.doPost)

    def init(self, request, action):
        groupChecks = GroupCheck.objects.filter(usser_id=request.user.pk)

        if groupChecks.exists() == False:
            raise PermissionDenied()

        return action(request, groupChecks)

    def doGet(self, request, groupChecks):
        task = groupChecks.first().main_task_id
        return self.responseData(request, task, groupChecks)


    def doPost(self, request, groupChecks):
        form = IdSelector(request.POST)
        task = None

        if form.is_valid():
            task = groupChecks.get(id=form.cleaned_data['id'])

        return self.responseData(request, task, groupChecks)

    def responseData(self, request, task, groupChecks):
        tasks, users, userTasksIds = self.collectDataObjects(task, groupChecks)
        data = {
            'tasks': tasks,
            'selected_task': task,
            'users': users,
            'userTasksIds': userTasksIds,
        }

        return render(request, 'tutor/tasks_to_be_checked.html', context=data)

    def collectDataObjects(self, task, groupChecks):
        groupCheckToShow = groupChecks.filter(main_task_id=task).first()
        tasks = []

        for groupCheck in groupChecks:
            task = groupCheck.main_task_id
            if task not in tasks:
                tasks.append(task)

        usersToCheck = groupCheckToShow.user_check_id
        users = User.objects.filter(id__in=usersToCheck)
        userTasks = UserTask.objects.filter(user_id__in=usersToCheck, main_task_id=task)
        userTasksIds = []

        for userTask in userTasks:
            userTasksIds.append(userTask.pk)

        return tasks, users, userTasksIds