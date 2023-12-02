from django.shortcuts import render, redirect
from django.views import View

from main.forms import UnitForm
from main.mixins.tutorRequired import TutorRequiredMixin


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class UnitCreate(TutorRequiredMixin, View):
    def get(self, request):
        return render(request, "content_bank/unit/edit.html", {'form': UnitForm()})

    def post(self, request):
        dict = {'name': request.Post.name,'tutor_id': request.user.pk}
        print(dict)
        # form = UnitForm(dict)
        #
        # if not form.is_valid():
        #     return render(request, "content_bank/unit/edit.html", {'form': form})
        #
        # form.save()

        return redirect('index')