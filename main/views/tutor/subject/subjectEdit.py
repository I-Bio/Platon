from django.shortcuts import render, redirect
from django.views import View

from main.forms import SubjectForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Subject


# @login_required(login_url='/login/', redirect_field_name=None)
# @user_passes_test(lambda u: u.is_staff, login_url='/index/', redirect_field_name=None)
class SubjectEdit(TutorRequiredMixin, View):
    def get(self, request, id):
        subject = Subject.objects.filter(pk=id)

        if not subject.exists():
            return render('index')

        form = SubjectForm(instance=subject.first())

        return render(request, "content_bank/subject_edit.html", {'form': form})

    def post(self, request, id):
        subject = Subject.objects.filter(pk=id)
        form = SubjectForm(request.POST, instance=subject.first())

        if not form.is_valid():
            return render(request, "content_bank/subject_edit.html", {'form': form})

        form.save()

        return redirect('index')