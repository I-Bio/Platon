from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from main.forms import StudentTaskForm
from main.models import Task, StudentFile


class TaskUpload(View):
    def get(self, request, task_id):

        return render(request, "students/checkTask/task_upload.html", {'form' : StudentTaskForm()})

    def post(self, request, task_id):
        form = StudentTaskForm(request.POST, request.FILES)

        if form.is_valid():
            self.createFiles(request, form, task_id)
        else:
            print("Пуська")

        return render(request, "students/checkTask/task_upload.html", {'form': StudentTaskForm()})

    def createFiles(self, request, form, task_id):
        files = form.cleaned_data["files"]
        print("Создало")

        for file in files:
            StudentFile.objects.create(creator=request.user.pk, task_id=task_id, file=file)
