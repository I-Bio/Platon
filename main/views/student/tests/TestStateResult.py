from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from django.views import View
from django.shortcuts import redirect, render
from main.models import Test, TestResult

class TestStateResult(View, StudentGroupRequiredMixin):
    def get (self, request):


        test = Test.objects.filter(name = request.user)

        if not test.exists():
            return redirect('index')

        test_result = TestResult.objects.filter(student=request.user, test=test.first())

        if not test_result.exists():
            return redirect('index')

        return render(request, "students/TestStateResult.html", {'result': test_result.first()})

    def post(self, request):
        ...