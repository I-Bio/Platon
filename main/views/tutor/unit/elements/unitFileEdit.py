from django.shortcuts import render, redirect
from django.views import View

from main.forms import FileForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import File, Unit
from main.views.MessageSuccess import MessageSuccess


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitFileEdit(TutorRequiredMixin, MessageSuccess, View):
    def get(self, request, unit_id, file_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        file = File.objects.filter(pk=file_id)

        if not file.exists():
            return redirect('index')

        form = FileForm(instance=file.first())

        return render(request, "content_bank/file/edit.html", {'form': form})

    def post(self, request, unit_id, file_id):
        file = File.objects.filter(pk=file_id)
        form = FileForm(request.POST, request.FILES, instance=file.first())

        if not form.is_valid():
            return render(request, "content_bank/file/edit.html", {'form': form})

        form.save()

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/file/edit.html", {'form': form})