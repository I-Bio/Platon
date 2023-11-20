from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Unit, Subject, UserTask, TestResult, User


class ShowGradeCardStudent(TutorRequiredMixin, View):
    def get(self, request, user_id, subject_id):
        unit_info = Unit.objects.filter(subject_id=subject_id)
        info_subject = Subject.objects.filter(id=subject_id).first()
        user_info = User.objects.filter(id=user_id).first()


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

        grade_tasks_lists = [UserTask.objects.filter(main_task_id=task.pk, user_id=user_id) for task in all_tasks]
        works_sets = []
        for list in grade_tasks_lists:
            for task in list:
                works_sets.append({'name_id': task.user_id.pk,
                                   'work_name': task.main_task_id.name,
                                   'grade': task.grade,
                                   'date': task.time_delivery})

        grade_tests_lists = [TestResult.objects.filter(test=task.pk, student=user_id) for task in all_tests]
        for list in grade_tests_lists:
            for test in list:
                works_sets.append({'name_id': test.student.pk,
                                   'work_name': test.test.name,
                                   'grade': test.result,
                                   'date': test.date})

        user = []

        print(works_sets)


        context = {
            'info_subject' : info_subject,
            'user_info' : user_info,
            'works_sets' : works_sets,
        }
        return render(request, 'students/StudentsTaskList/grade_card_list_student.html', context=context)