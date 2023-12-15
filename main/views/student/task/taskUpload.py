from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from django.views import View

from main.forms import StudentTaskForm
from main.models import Task, StudentFile, UserTask, User, Unit, Subject, StudentGroup


class TaskUpload(View):
    def get(self, request, task_id):
        return render(request, "students/checkTask/task_upload.html", {'form': StudentTaskForm(), 'task_id': task_id})

    def post(self, request, task_id):
        form = StudentTaskForm(request.POST, request.FILES)

        if form.is_valid():
            print("Valid")
            self.createFiles(request, form, task_id)
            task = Task.objects.filter(id=task_id).first()
            user = User.objects.filter(id=request.user.pk).first()
            stud_group = StudentGroup.objects.filter(id=user.groups.all().first().pk).first()
            own_grade = form.cleaned_data['own_grade']
            UserTask.objects.create(last_name=user.last_name, group_id=stud_group, first_name=user.first_name,
                                    user_id=user, main_task_id=task, own_grade=own_grade)

            return JsonResponse({"url" : reverse("index")}, safe=False)
        else:
            print(request.POST, request.FILES)
            form = StudentTaskForm()

        return render(request, "students/checkTask/task_upload.html", {'form': form, 'task_id': task_id})

    def createFiles(self, request, form, task_id):
        files = form.cleaned_data["files"]

        for file in files:
            file_info = StudentFile(creator=request.user.pk, task_id=task_id, file=file)
            file_info.save()
