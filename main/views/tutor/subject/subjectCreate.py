from django.shortcuts import render, redirect
from django.views import View

from main.forms import SubjectForm
from main.mixins.tutorRequired import TutorRequiredMixin


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class SubjectCreate(TutorRequiredMixin, View):
    def get(self, request):

        return render(request, "content_bank/subject_edit.html", {'form': SubjectForm()})

    def post(self, request):

        dict = {
            'name' : request.POST['name'],
            'tutor_id' : request.user.pk,
        }

        form = SubjectForm(dict)

        if not form.is_valid():
            return render(request, "content_bank/subject_edit.html", {'form': form})

        form.save()

        return redirect('index')
