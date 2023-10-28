from django.shortcuts import render, redirect
from django.views import View

from main.forms import UnitForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitEdit(TutorRequiredMixin, View):
    def get(self, request, id):
        unit = Unit.objects.filter(pk=id)

        if not unit.exists():
            return render('index')

        form = UnitForm(instance=unit.first())

        return render(request, "content_bank/unit/edit.html", {'form': form})

    def post(self, request, id):
        unit = Unit.objects.filter(pk=id)
        form = UnitForm(request.POST, instance=unit.first())

        if not form.is_valid():
            return render(request, "content_bank/unit/edit.html", {'form': form})

        form.save()

        return redirect('index')