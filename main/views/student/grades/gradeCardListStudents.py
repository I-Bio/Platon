from django.shortcuts import render
from django.views import View

from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from main.models import Unit, Subject, UserTask, TestResult, User, StudentGroup


class ShowGradeCardStudent(StudentGroupRequiredMixin, View):
    def get(self, request):
        tutor_grade_weight, student_grade_weight, own_grade_weight = 0.85, 0.1, 0.05
        

        subjects_all = Subject.objects.all()

        user = User.objects.filter(id=request.user.pk).first()
        group_user_id = user.groups.first().pk

        where_is_sudent_in_subject = []
        for subject in subjects_all:
            if group_user_id in subject.enrolled_groups_id:
                where_is_sudent_in_subject.append(subject)


        unit_all = Unit.objects.filter(subject__in=where_is_sudent_in_subject)

        all_task_list = [i.tasks.all() for i in unit_all]
        all_tasks = []
        for list in all_task_list:
            for task in list:
                all_tasks.append(task)

        all_test_list = [i.tests.all() for i in unit_all]
        all_tests = []
        for list in all_test_list:
            for task in list:
                all_tests.append(task)


        user_tasks = UserTask.objects.filter(user_id=request.user.pk)
        user_tests = TestResult.objects.filter(student=request.user.pk)
        works_sets = []

        user_task_id_list = []
        for user_task in user_tasks:
            user_task_id_list.append(user_task.main_task_id)

        user_test_id_list = []
        for user_test in user_tests:
            user_test_id_list.append(user_test.test)


        for task in all_tasks:
            if task in user_task_id_list:
                date = user_tasks.filter(main_task_id=task.pk).first().time_delivery
                grade_info = user_tasks.filter(main_task_id=task.pk).first()
                grade = grade_info.grade * tutor_grade_weight + grade_info.checker_grade * student_grade_weight + grade_info.own_grade * own_grade_weight
            else:
                grade = 'работа ны выполнена'
                date = 'None'

            works_sets.append({
                'subject': unit_all.filter(tasks=task).first().subject,
                'work_name': task.name,
                'grade': grade,
                'date': date,
            })


        for test in all_tests:
            if test in user_test_id_list:
                    grade = user_tests.filter(test=test.pk).first().result
                    date = user_tests.filter(test=test.pk).first().date
            else:
                    grade = 'работа ны выполнена'
                    date = 'None'

            works_sets.append({
                'subject': unit_all.filter(tests=test).first().subject,
                'work_name': test.name,
                'grade': grade,
                'date': date,
            })


        grade_card_list = []
        for sub in where_is_sudent_in_subject:
            works = []
            for work in works_sets:
                if sub == work['subject']:
                    works.append({'work_name': work['work_name'],
                                  'grade': work['grade'],
                                  'date': work['date']
                                  })

            grade_card_list.append({
                'subject' : sub,
                'works' : works,
            })

        context = {
            'grade_card_list': grade_card_list,
            'where_is_sudent_in_subject' : where_is_sudent_in_subject,
            'user' : user,
        }
        return render(request, 'students/StudentsTaskList/grade_card_list_student.html', context=context)