from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from main import models
from main.forms import TestForm
from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit, Question
from main.views.MessageSuccess import MessageSuccess


#@method_decorator(user_passes_test, name="dispatch")
class UnitTestEdit(LoginRequiredMixin, TutorRequiredMixin, MessageSuccess, View):
    login_url = '/login/'
    redirect_field_name = None

    def get(self, request: HttpRequest, unit_id, test_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        test = models.Test.objects.filter(pk=test_id)

        if not test.exists():
            return redirect('index')

        form = TestForm(instance=test.first())

        return render(request, "content_bank/test/edit.html", {
            'form': form,
            'questions': Question.objects.exclude(id__in=test.first().questions.all())})

    def post(self, request: HttpRequest, unit_id, test_id):
        test = models.Test.objects.filter(pk=test_id)

        form = TestForm(request.POST, instance=test.first())

        if not form.is_valid():
            print(form.data)
            print(form.errors)

            return render(request, "content_bank/test/edit.html",
                          {'form': form, 'questions': Question.objects.exclude(id__in=test.first().questions.all())})

        form.save()

        self.get_message_success(request)

        if 'saveAndReturn' in request.POST:
            print("Okkk")
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/test/edit.html",
                      {'form': form, 'questions': Question.objects.exclude(id__in=test.first().questions.all())})

