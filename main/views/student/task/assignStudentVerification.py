from django.shortcuts import render, redirect
from django.views import View

from main.forms import StudentSelectForm
from main.models import GroupCheck


class AssignStudent(View):

    def get(self, request):
        form = StudentSelectForm()
        return render(request, 'students/checkTask/select_student.html', {'form': form})

    def post(self, request):

        if request.method == 'POST':
            form = StudentSelectForm(request.POST)

        if form.is_valid():
            selected_group = form.cleaned_data['group']
            selected_student = form.cleaned_data['student']

            if request.POST['action'] == 'add':
                GroupCheck.objects.create(usser_id=selected_student.pk, group_check=selected_group.pk)
            elif request.POST['action'] == 'delite':
                GroupCheck.objects.filter(usser_id=selected_student.pk).delete()
        return redirect('assign_for_review')


