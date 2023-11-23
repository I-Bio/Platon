from django.views.generic import View
from django.shortcuts import render, redirect

from main.forms import AddGradeForm
from main.models import UserTask, StudentFile

from django.http import Http404


class AddGradeView(View):

    def get(self, request, user_id: int, main_task_id: int):
        try:
            user = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
            print(user)
            files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)

        except (UserTask.DoesNotExist, StudentFile.DoesNotExist):
            raise Http404

        return render(request, template_name="tutor/addGrade.html",
                      context={'form': AddGradeForm, 'user': user, 'files': files})

    def post(self, request, user_id: int, main_task_id: int):
        user = UserTask.objects.filter(user_id=user_id, main_task_id=main_task_id).first()
        files = StudentFile.objects.filter(creator=user_id, task_id=main_task_id)
        form = AddGradeForm(request.POST)

        if not form.is_valid():
            return render(request, template_name="tutor/addGrade.html",
                          context={'form': form, 'user_id': user_id, 'user': user, 'files': files})

        form.save(user=user)

        if 'selectForReviewButton' in request.POST:
            return redirect('', kwargs={'user': user})

        return render(request, template_name="tutor/addGrade.html",
                      context={'form': form, 'user_id': user_id, 'grade': user.grade, 'user': user, 'files': files})
