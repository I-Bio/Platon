from django.shortcuts import redirect, render
from django.views import View

from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from main.models import Unit, Test, TestResult


# @login_required(login_url='/login/', redirect_field_name=None)
class TestResultDisplay(View, StudentGroupRequiredMixin):
    def get(self, request, unit_id, test_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        test = Test.objects.filter(pk=test_id)

        if not test.exists():
            return redirect('index')

        test_result = TestResult.objects.filter(student=request.user, test=test.first())

        if not test_result.exists():
            return redirect('index')

        return render(request, "content_bank/test/result.html", {'result': test_result.first(), 'unit': unit.first()})

    def post(self, request, unit_id, test_id):
        ...
