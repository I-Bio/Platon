from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from main.forms import StudentTaskForm
from main.models import Task, StudentFile, UserTask, User, StudentGroup
from main.views.MessageSuccess import MessageSuccess


class TaskUpload(View, MessageSuccess):
    def get(self, request, task_id):
        return render(request, "students/checkTask/task_upload.html", {'form': StudentTaskForm(), 'task_id': task_id})

    def post(self, request, task_id):
        form = StudentTaskForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            task = Task.objects.filter(id=task_id).first()
            user = User.objects.filter(id=user.pk).first()
            stud_group = StudentGroup.objects.get(name=user.groups.first())
            own_grade = form.cleaned_data['own_grade']
            currentUserTask = UserTask.objects.filter(user_id=user, main_task_id=task).first()

            if (currentUserTask == None):
                UserTask.objects.create(last_name=user.last_name, group_id=stud_group, first_name=user.first_name,
                                        user_id=user, main_task_id=task, own_grade=own_grade)
            else:
                currentUserTask.own_grade = own_grade
                currentUserTask.save()
                self.deleteFiles(task_id, user.pk)

            self.createFiles(form, user.pk, task_id)

            self.get_message_success(request)

            print("dwdwd")
            # return JsonResponse({"url": reverse("index")}, safe=False)
        else:
            form = StudentTaskForm()
        return render(request, "students/checkTask/task_upload.html", {'form': form, 'task_id': task_id})

    def createFiles(self, form, user_id, task_id):
        files = form.cleaned_data["files"]

        for file in files:
            StudentFile.objects.create(creator=user_id, task_id=task_id, file=file)

    def deleteFiles(self, task_id, user_id):
        files = StudentFile.objects.filter(task_id=task_id, creator=user_id)

        for file in files:
            file.delete()
