from django.views.generic import View
from django.shortcuts import render, redirect

from main.forms import AddGradeForm, AddGradeStudentForm
from main.models import UserTask, StudentFile, Task, User

from django.http import Http404


class AddGradeView(View):

    def get(self, request, user_id: int, main_task_id: int):
        try:
            user = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
            files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)
            task_name = Task.objects.filter(id=main_task_id).first()
        except (UserTask.DoesNotExist, StudentFile.DoesNotExist):
            raise Http404


        context = {

            'form': AddGradeForm,
            'user': user,
            'files': files,
            'task_name' : task_name,
        }

        return render(request, template_name="tutor/addGrade.html", context=context)

    def post(self, request, user_id: int, main_task_id: int):
        user = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
        files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)

        if request.user.is_tutor or request.user.is_staff:
            form = AddGradeForm(request.POST)
        else:
            form = AddGradeStudentForm(request.POST)



        if not form.is_valid():
            return render(request, template_name="tutor/addGrade.html",
                          context={'form': form, 'user_id': user_id, 'user': user, 'files': files})

        form.save(user)

        if 'selectForReviewButton' in request.POST:
            return redirect('', kwargs={'user': user})


        return render(request, template_name="tutor/addGrade.html",
                      context={'form': form, 'user_id': user_id, 'grade': user.grade, 'user': user, 'files': files})
