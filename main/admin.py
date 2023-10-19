from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(StudentGroup)

admin.site.register((Test, Question, QuestionOption))
admin.site.register((Unit, Lecture, Reference, File, Task))
admin.site.register((TestResult))
admin.site.register((Subject))
admin.site.register((Papa))