import os

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from Platon import settings


class TeacherManualView(View):
    def get(self, request):
        return render(request, 'tutor/manual_for_teacher.html')

    def post(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, 'file/manual.docx')
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="manual.docx"'
            return response
