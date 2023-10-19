from django.shortcuts import render, redirect
from django.views import View

from main.forms import UnitForm


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitCreate(View):
    def get(self, request):
        return render(request, "content_bank/unit/edit.html", {'form': UnitForm()})

    def post(self, request):
        form = UnitForm(request.POST)

        if not form.is_valid():
            return render(request, "content_bank/unit/edit.html", {'form': form})

        form.save()

        return redirect('index')