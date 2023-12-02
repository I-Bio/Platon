from django.contrib import admin
from .models import *


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Unit)
class AuthorAdmin(admin.ModelAdmin):
    filter_horizontal = ('lectures', 'references', 'files', 'tests', 'tasks')


admin.site.register(StudentFile)
admin.site.register((Test, Question, QuestionOption))
admin.site.register((Lecture, Reference, File, Task))
admin.site.register((TestResult))
admin.site.register((Subject))
admin.site.register((Papa))
admin.site.register((RegistrationLinks))
admin.site.register((StudentGroup))
admin.site.register((UserTask))
admin.site.register((Notification))
