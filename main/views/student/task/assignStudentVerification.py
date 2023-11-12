from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from main.forms import ChooseStudentsToChecker
from main.models import GroupCheck, User, Task, StudentGroup


class AssignStudent(View):


    def get(self, request, user_id, main_task_id, group_id):

        info_group_id = StudentGroup.objects.filter(id=group_id)[0]
        info_user_id = User.objects.filter(id=user_id)[0]
        info_users_id = User.objects.filter(groups=group_id)





        context = {
            'info_user_id' : info_user_id,
            'info_users_id' : info_users_id,

            'user_id' : user_id,
            'main_task_id': main_task_id,
            'group_id' : group_id,

        }
        return render(request, 'students/checkTask/select_student.html', context=context)
    def post(self, request, user_id, main_task_id, group_id):
        list_checker_student = request.POST.getlist('questions[]')
        print(list_checker_student)
        form = ChooseStudentsToChecker(request.POST)

        if form.is_valid() == True:
            context = {
                'form': form,
                'questions': GroupCheck.objects.all(),

                'user_id': user_id,
                'main_task_id': main_task_id,
                'group_id': group_id,
            }

            return render(request, "students/checkTask/select_student.html", context=context)
        A
        return redirect('select_students', user_id=user_id, main_task_id=main_task_id, group_id=group_id)

        ...
#     def get(self, request, group_id, main_task_id):
#         task = Task.objects.filter(pk=main_task_id)
#         group = StudentGroup.objects.filter(pk=group_id)
#         students = User.objects.filter(studyGroup=group_id)
#
#
#         context = {
#             'students' : students,
#             'task' : task[0],
#             'group' : group[0],
#
#
#             'group_id' : group_id,
#             'main_task_id' : main_task_id,
#         }
#         return render(request, 'students/checkTask/select_student.html', context=context)
#
#     def post(self, request, group_id, main_task_id):
#         if request.method == "POST":
#
#             selected_students = list(map(int, request.POST.getlist("student")))
#             selected_students_check = list(map(int, request.POST.getlist("student_check")))
#
#
#             for user_check in selected_students_check:
#                 g = GroupCheck(usser_id=user_check, group_check=group_id, main_task_id=Task.objects.filter(id = main_task_id)[0].id, user_check_id=selected_students)
#                 g.save()
#             # print(f'selected_students = {selected_students}')
#             # print(f'selected_students_check = {selected_students_check}')
#
#             return redirect('select_students', group_id=group_id, main_task_id=main_task_id)
#
#
