from django.contrib import admin
from .models import *


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Unit)
class AuthorAdmin(admin.ModelAdmin):
    filter_horizontal = ('lectures', 'references', 'files', 'tests', 'tasks')


models_to_register = (
    StudentFile, Test, Question, QuestionOption, Lecture, Reference, File, Task, TestResult, Subject, RegistrationLinks,
    StudentGroup, TutorGroup, AdminGroup, UserTask, GroupCheck, Notification)
admin.site.register(models_to_register)
