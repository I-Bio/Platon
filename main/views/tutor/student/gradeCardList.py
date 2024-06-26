from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import StudentGroup, Subject, Task, UserTask, Unit, TestResult, User


class ShowGradeCardList(TutorRequiredMixin, View):
    def get(self, request, group_id, subject_id):

        tutor_grade_weight, student_grade_weight, own_grade_weight = 0.85, 0.1, 0.05

        info_group = StudentGroup.objects.filter(name=group_id).first()

        info_task_user = User.objects.filter(groups=group_id)
        unit_info = Unit.objects.filter(subject_id=subject_id)


        info_subject = Subject.objects.filter(id=subject_id).first()

        if info_subject == None:
            raise Http404()

        if request.user.pk != info_subject.tutor_id.pk:
            raise PermissionDenied()



        all_task_list = [i.tasks.all() for i in unit_info]
        all_tasks = []
        for list in all_task_list:
            for task in list:
                all_tasks.append(task)

        all_test_list = [i.tests.all() for i in unit_info]
        all_tests = []
        for list in all_test_list:
            for task in list:
                all_tests.append(task)


        grade_tasks_lists = [UserTask.objects.filter(main_task_id=task.pk) for task in all_tasks]
        works_sets = []
        for list in grade_tasks_lists:
            for task in list:
                grade = task.grade * tutor_grade_weight + task.checker_grade * student_grade_weight + task.own_grade * own_grade_weight
                works_sets.append({'name_id' : task.user_id.pk,
                                   'work_name' : task.main_task_id.name,
                                   'grade' : grade,
                                   'date' : task.time_delivery})

        grade_tests_lists = [TestResult.objects.filter(test=task.pk) for task in all_tests]
        for list in grade_tests_lists:
            for test in list:
                works_sets.append({'name_id': test.student.pk,
                                   'work_name': test.test.name,
                                   'grade': test.get_score(),
                                    'date': test.date})

        users = []
        for user in info_task_user:
            works = []
            for work in works_sets:
                 if user.pk == work['name_id']:
                    works.append({'work_name': work['work_name'],
                                   'grade': work['grade'],
                                    'date': work['date']})

            users.append({'name': f"{user.last_name} {user.first_name}",
                          'works' : works})

        data_list = []
        for entry in users:
            for work_entry in entry['works']:
                date = datetime.strptime(str(work_entry['date'])[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
                data_list.append({
                    'Name': entry['name'],
                    'Work Name': work_entry['work_name'],
                    'Grade': work_entry['grade'],
                    'Date': date
                })

        df = pd.DataFrame(data_list)

        df.to_excel('media/output.xlsx', index=False)

        context = {
            'info_group_name' : info_group,
            'info_subject' : info_subject,
            'info_task_user' : info_task_user,
            'users' : users,
            'group_id': group_id,
            'subject_id': subject_id,
        }
        return render(request, 'tutor/grade_card.html', context=context)

    def post(self, request, group_id, subject_id):
        if request.method == 'POST':
            with open('media/output.xlsx', 'rb') as excel_file:
                response = HttpResponse(excel_file.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=output.xlsx'
                return response