from django.views import View
from django.shortcuts import render
from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from main.models import TestResult, StudentGroup, User


class ShowTestsStateDisplay(StudentGroupRequiredMixin, View):
    def get(self, request):

        groups = StudentGroup.objects.all()
        users = User.objects.filter()
        tests = TestResult.objects.all()

        user_list = []
        for user in users:
            for group in groups:
                if str(user.groups.first()) == str(group):
                    user_list.append(user)

        works_list = []
        name = 'не выполнил'
        for user in user_list:
            for test in tests:
                if str(test.test.name) == str(user):
                    test = test.result
                else:
                    test = name
            works_list.append({'user' : user,
                               'test' : test})




        return render(request, 'admin/test_state_display.html', context = {"works_list" : works_list})
    def post(self, request):
        ...