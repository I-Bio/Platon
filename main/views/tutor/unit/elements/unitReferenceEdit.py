from django.shortcuts import redirect, render
from django.views import View

from main.forms import ReferenceForm
from main.models import Unit, Reference


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitReferenceEdit(View):
    def get(self, request, unit_id, reference_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        reference = Reference.objects.filter(pk=reference_id)

        if not reference.exists():
            return redirect('index')

        form = ReferenceForm(instance=reference.first())

        return render(request, "content_bank/reference/edit.html", {'form': form})

    def post(self, request, unit_id, reference_id):
        reference = Reference.objects.filter(pk=reference_id)
        form = ReferenceForm(request.POST, instance=reference.first())

        if not form.is_valid():
            return render(request, "content_bank/reference/edit.html", {'form': form})

        form.save()

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/reference/edit.html", {'form': form})