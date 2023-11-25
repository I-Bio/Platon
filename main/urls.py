import uuid

from django.urls import path
from main.views.student.tests.testResultDisplay import TestResultDisplay
from main.views.student.tests.testStudentTesting import TestStudentTesting
from main.views.tutor.unit.elements.unitLectureEdit import UnitLectureEdit
from main.views.tutor.unit.elements.unitTaskCreate import UnitTaskCreate
from main.views.tutor.unit.elements.unitTaskEdit import UnitTaskEdit
from main.views.tutor.unit.elements.unitTestEdit import UnitTestEdit
from main.views.tutor.unit.elements.unitTestCreate import UnitTestCreate
from main.views.general.index import Index
from .views.admin.AddGroupUserView import AddGroupUserView

from .views.authenticate.login import Login
from .views.authenticate.registration import Registration
from .views.notification.noticationMenuView import NotificationMenuView
from .views.student.grades.gradeCardListStudents import ShowGradeCardStudent
from .views.student.grades.studentOwnGrades import StudentOwnGrades
from .views.student.task.assignStudentVerification import AssignStudent
from .views.student.task.showAndEstimateGrade import GradeTask
from .views.student.task.showWorkStudents import StudentsWorkList
from .views.student.task.taskUpload import TaskUpload
from .views.tutor.link.createInviteLinkView import CreateInviteLinkView
from .views.tutor.student.gradeCardList import ShowGradeCardList

from .views.tutor.student.grades.studentGradeChanger import StudentGradeChanger
from .views.tutor.student.grades.studentGrades import StudentGrades
from .views.tutor.student.groupsList import GroupsList
from .views.tutor.student.studentsList import StudentsList
from .views.tutor.subject.subjectCreate import SubjectCreate
from .views.tutor.subject.subjectEdit import SubjectEdit
from .views.tutor.task.addGradeView import AddGradeView
from .views.tutor.task.showUncompletedTasks import showUncompletedTasks
from .views.tutor.unit.elements.unitFileCreate import UnitFileCreate
from .views.tutor.unit.elements.unitFileEdit import UnitFileEdit
from .views.tutor.unit.elements.unitLectureCreate import UnitLectureCreate
from .views.tutor.unit.elements.unitReferenceCreate import UnitReferenceCreate
from .views.tutor.unit.elements.unitReferenceEdit import UnitReferenceEdit
from .views.tutor.unit.questions.questionCreate import QuestionCreate
from .views.tutor.unit.questions.questionEdit import QuestionEdit
from .views.tutor.unit.questions.questionsList import QuestionsList
from .views.tutor.unit.unitCreate import UnitCreate
from .views.tutor.unit.unitEdit import UnitEdit
from main.views.general.unitContent import UnitContent

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('registration/<str:key>', Registration.as_view(), name="registration"),

    path('', Index.as_view(), name="index"),

    path('grades/', StudentOwnGrades.as_view(), name="own_grades"),

    path('groups/', GroupsList.as_view(), name="groups_list"),
    path('students/<int:group_pk>', StudentsList.as_view(), name="students_list"),
    path('student_grades/<int:student_pk>', StudentGrades.as_view(), name="student_grades"),
    path('student_grades/<int:student_pk>/change/<int:grade_pk>', StudentGradeChanger.as_view(),
         name="student_grade_change"),

    path('questions/list/', QuestionsList.as_view(), name='questions_list'),
    path('questions/create/', QuestionCreate.as_view(), name='question_create'),
    path('questions/edit/<int:id>/', QuestionEdit.as_view(), name='question_edit'),

    path('subjects/create/', SubjectCreate.as_view(), name='subject_create'),
    path('subjects/edit/<int:id>/', SubjectEdit.as_view(), name='subject_edit'),

    path('units/create/', UnitCreate.as_view(), name='unit_create'),
    path('units/edit/<int:id>/', UnitEdit.as_view(), name='unit_edit'),

    path('unit/<int:unit_id>/', UnitContent.as_view(), name='unit_content'),

    path('unit/<int:unit_id>/lecture/create/', UnitLectureCreate.as_view(), name='unit_lecture_create'),
    path('unit/<int:unit_id>/lecture/edit/<int:lecture_id>/', UnitLectureEdit.as_view(), name='unit_lecture_edit'),

    path('unit/<int:unit_id>/reference/create/', UnitReferenceCreate.as_view(), name='unit_reference_create'),
    path('unit/<int:unit_id>/reference/edit/<int:reference_id>/', UnitReferenceEdit.as_view(),
         name='unit_reference_edit'),

    path('unit/<int:unit_id>/file/create/', UnitFileCreate.as_view(), name='unit_file_create'),
    path('unit/<int:unit_id>/file/edit/<int:file_id>/', UnitFileEdit.as_view(), name='unit_file_edit'),

    path('unit/<int:unit_id>/test/create/', UnitTestCreate.as_view(), name='unit_test_create'),
    path('unit/<int:unit_id>/test/edit/<int:test_id>/', UnitTestEdit.as_view(), name='unit_test_edit'),
    path('testing/<int:unit_id>/<int:test_id>/', TestStudentTesting.as_view(), name='test_testing'),
    path('testing/<int:unit_id>/<int:test_id>/result', TestResultDisplay.as_view(), name='test_result'),

    path('unit/<int:unit_id>/task/create/', UnitTaskCreate.as_view(), name='unit_task_create'),
    path('unit/<int:unit_id>/task/edit/<int:task_id>/', UnitTaskEdit.as_view(), name='unit_task_edit'),

    path('grade/<int:user_id>/<int:main_task_id>/<int:who_check>', GradeTask.as_view(), name='grade_group'),

    path('add_group_user/', AddGroupUserView.as_view(), name='add_group_user'),

    path('completed_and_notcompleted_work/<int:task_id>/<int:group_id>', StudentsWorkList.as_view(),
         name='completed_and_notcompleted_work'), #EDRGVEWRGWSERBWR

    path('assign_for_review/<int:user_id>/<int:main_task_id>', AssignStudent.as_view(), name='select_students'),

    path('show_grade_card_list/<int:group_id>/<int:subject_id>', ShowGradeCardList.as_view(),
         name='show_grade_card_list'),
    path('show_grade_card_list_students/<int:user_id>/', ShowGradeCardStudent.as_view(),
         name='show_grade_card_list_students'),

    path('taskTest/<int:task_id>', TaskUpload.as_view(), name='student_task_upload'),

    path('add_grade/<int:user_id>/<int:main_task_id>', AddGradeView.as_view(), name='add_grade'),

    path('create_invite_link/', CreateInviteLinkView.as_view(), name='create_invite_link'),

    path('notification_menu/', NotificationMenuView.as_view(), name='notification_menu'),

    path('tasks_to_check/<int:main_task_id>/', showUncompletedTasks.as_view(), name='tasks_to_check')
]
