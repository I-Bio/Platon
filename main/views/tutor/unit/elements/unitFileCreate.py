from django.shortcuts import redirect, render
from django.views import View

from main.forms import FileForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit
from main.views.MessageSuccess import MessageSuccess


class UnitFileCreate(TutorRequiredMixin, MessageSuccess, View):
    def get(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        return render(request, "content_bank/file/edit.html", {'form': FileForm()})

    def post(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id).first()
        form = FileForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, "content_bank/file/edit.html", {'form': form})

        form.save()

        unit.files.add(form.instance)

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return redirect('unit_file_edit', unit.pk, form.instance.pk)