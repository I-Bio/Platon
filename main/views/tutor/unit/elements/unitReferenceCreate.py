from django.shortcuts import redirect, render
from django.views import View

from main.forms import ReferenceForm
from main.models import Unit


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitReferenceCreate(View):
    def get(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        return render(request, "content_bank/reference/edit.html", {'form': ReferenceForm()})

    def post(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id).first()
        form = ReferenceForm(request.POST)

        if not form.is_valid():
            return render(request, "content_bank/reference/edit.html", {'form': form})

        form.save()

        unit.references.add(form.instance)

        if 'saveAndReturn' in request.POST:
            return redirect('unit_content', unit_id)

        return redirect('unit_reference_edit', unit.pk, form.instance.pk)