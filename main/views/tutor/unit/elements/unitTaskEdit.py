from django.shortcuts import redirect, render
from django.views import View

from main.forms import TaskForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit, Task
from main.views.MessageSuccess import MessageSuccess


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitTaskEdit(TutorRequiredMixin, MessageSuccess, View):
    def get(self, request, unit_id, task_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        task = Task.objects.filter(pk=task_id)

        if not task.exists():
            return redirect('index')

        form = TaskForm(instance=task.first())

        return render(request, "content_bank/task/edit.html", {'form': form})

    def post(self, request, unit_id, task_id):
        task = Task.objects.filter(pk=task_id)
        form = TaskForm(request.POST, instance=task.first())

        if not form.is_valid():
            return render(request, "content_bank/task/edit.html", {'form': form})

        form.save()

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/task/edit.html", {'form': form})
