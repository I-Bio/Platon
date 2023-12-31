from django.views.generic import View
from django.shortcuts import render, redirect

from main.forms import AddGradeForm, AddGradeStudentForm
from main.models import UserTask, StudentFile, Task, User, Notification

from django.http import Http404


class AddGradeView(View):

    def get(self, request, user_id: int, main_task_id: int):
        try:
            userTask = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
            files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)
            user = request.user
            task_name = Task.objects.filter(id=main_task_id).first()
        except (UserTask.DoesNotExist, StudentFile.DoesNotExist):
            raise Http404

        context = {
            'form': AddGradeForm,
            'user_id': user_id,
            'userTask': userTask,
            'files': files,
            'task_name': task_name,
        }

        return render(request, template_name="tutor/addGrade.html", context=context)

    def post(self, request, user_id: int, main_task_id: int):
        userTask = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
        files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)
        user = request.user

        if user.is_tutor or user.is_staff:
            form = AddGradeForm(request.POST)
        else:
            form = AddGradeStudentForm(request.POST)

        if not form.is_valid():
            return render(request, template_name="tutor/addGrade.html",
                          context={'form': form, 'user_id': user_id, 'user': user, 'userTask': userTask,
                                   'files': files})

        form.save(userTask)

        task = userTask.main_task_id
        grade = form.cleaned_data['grade']
        notification_header = f"Вам выставлена оценка за задание '{task}'"
        notification_body = f"Вам выставлена оценка {grade} по дисциплине '{task.unit_set.all().first().subject}' за задание '{task}'"
        notification = Notification.objects.create(
            header=notification_header,
            body=notification_body,
            user_id=userTask.user_id
        )

        return render(request, template_name="tutor/addGrade.html",
                      context={'form': form,
                               'user_id': user_id,
                               'grade': userTask.grade,
                               'userTask': userTask,
                               'files': files})
