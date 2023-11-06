from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


from main.models import GroupCheck, User, Task, StudentGroup


class AssignStudent(View):

    def get(self, request, group_id, main_task_id):
        task = Task.objects.filter(pk=main_task_id)
        group = StudentGroup.objects.filter(pk=group_id)
        students = User.objects.filter(studyGroup=group_id)


        context = {
            'students' : students,
            'task' : task[0],
            'group' : group[0],


            'group_id' : group_id,
            'main_task_id' : main_task_id,
        }
        return render(request, 'students/checkTask/select_student.html', context=context)

    def post(self, request, group_id, main_task_id):
        if request.method == "POST":

            selected_students = list(map(int, request.POST.getlist("student")))
            selected_students_check = list(map(int, request.POST.getlist("student_check")))


            for user_check in selected_students_check:
                g = GroupCheck(usser_id=user_check, group_check=group_id, main_task_id=Task.objects.filter(id = main_task_id)[0].id, user_check_id=selected_students)
                g.save()
            # print(f'selected_students = {selected_students}')
            # print(f'selected_students_check = {selected_students_check}')

            return redirect('select_students', group_id=group_id, main_task_id=main_task_id)


    #     if request.method == 'POST':
    #         form = GroupSelectionForm(request.POST)
    #         if form.is_valid():
    #         selected_group = form.cleaned_data['group']
    #             students = User.objects.filter(studyGroup=selected_group
    #     else:
    #         form = GroupSelectionForm()
    #
    #
    #     return render(request, 'students/checkTask/select_student.html', {'form': form, 'students': students})


