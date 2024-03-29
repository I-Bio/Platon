from django.shortcuts import redirect, render
from django.views import View

from main.forms import LectureForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit
from main.views.MessageSuccess import MessageSuccess


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitLectureCreate(TutorRequiredMixin, MessageSuccess, View):
    def get(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        return render(request, "content_bank/lecture/edit.html", {'form': LectureForm()})

    def post(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id).first()
        form = LectureForm(request.POST)

        if not form.is_valid():
            return render(request, "content_bank/lecture/edit.html", {'form': form})

        form.save()

        unit.lectures.add(form.instance)

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return redirect('unit_lecture_edit', unit.pk, form.instance.pk)

