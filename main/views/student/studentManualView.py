from django.shortcuts import render
from django.views import View


class StudentManualView(View):
    def get(self, request):
        return render(request, 'students/manual_for_student.html')
