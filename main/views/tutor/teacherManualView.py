from django.shortcuts import render
from django.views import View


class TeacherManualView(View):
    def get(self, request):
        return render(request, 'tutor/manual_for_teacher.html')