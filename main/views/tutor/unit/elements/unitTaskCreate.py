from django.shortcuts import redirect, render
from django.views import View

from main.forms import TaskForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit, User, Notification


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitTaskCreate(TutorRequiredMixin, View):
    def get(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        return render(request, "content_bank/task/edit.html", {'form': TaskForm()})

    def post(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id)
        unit = unit.first()

        form = TaskForm(request.POST)

        if not form.is_valid():
            return render(request, "content_bank/task/edit.html", {'form': form})

        form.save()

        unit.tasks.add(form.instance)

        enrolled_groups_id = unit.subject.enrolled_groups_id
        users = User.objects.filter(groups__in=enrolled_groups_id)
        notification_header = "Появилось задание"
        notification_body = f"Появилось задание по дисциплине '{unit.subject.name}'"

        for user in users:
            notification = Notification.objects.create(
                header=notification_header,
                body=notification_body,
                user_id=user
            )

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return redirect('unit_task_edit', unit.pk, form.instance.pk)