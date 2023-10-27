from django.shortcuts import render, redirect
from django.views import View

from main.forms import StudentSelectForm


class AssignStudent(View):

    def get(self, request):
        if request.method == 'POST':
            form = StudentSelectForm(request.POST)
            if form.is_valid():
                selected_student = form.cleaned_data['student']
                return redirect('review', student_id=selected_student.id)
        else:
            form = StudentSelectForm()
        return render(request, 'students/checkTask/select_student.html', {'form' : form})