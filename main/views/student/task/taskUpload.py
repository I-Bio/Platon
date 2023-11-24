from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from main.forms import StudentTaskForm
from main.models import Task, StudentFile, UserTask, User, Unit, Subject, StudentGroup


class TaskUpload(View):
    def get(self, request, task_id):
        info_unit = Unit.objects.all()
        #проверка на доступ к курсу
        for theme in info_unit:
            for task in theme.tasks.all():

                if task_id == task.pk:
                    subject = theme.subject

        if (request.user.pk in subject.users_id) == False:
            return HttpResponse(status=403)

        return render(request, "students/checkTask/task_upload.html", {'form' : StudentTaskForm(), 'task_id' : task_id})

    def post(self, request, task_id):
        form = StudentTaskForm(request.POST, request.FILES)
        if form.is_valid():
            self.createFiles(request, form, task_id)
            user = User.objects.filter(id=request.user.pk).first()
            task = Task.objects.filter(id=task_id).first()
            stud_group = StudentGroup.objects.filter(id=user.groups.all().first().pk).first()
            own_grade = form.cleaned_data['own_grade']
            UserTask.objects.create(last_name=user.last_name, group_id=stud_group , first_name=user.first_name, user_id=user, main_task_id=task, own_grade=own_grade)
            return HttpResponse('Успешно')
        else:
            form = StudentTaskForm()



        return render(request, "students/checkTask/task_upload.html", {'form': form, 'task_id' : task_id})

    def createFiles(self, request, form, task_id):
        files = form.cleaned_data["files"]


        for file in files:
            file_info = StudentFile(creator=request.user.pk, task_id=task_id, file=file)
            file_info.save()

