import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



def score_to_grade(score):
    if score > 90:
        return 5
    if score > 80:
        return 4
    if score > 60:
        return 3
    return 2


class StudentGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TutorGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AdminGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class RegistrationLinks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    group_name = models.CharField(max_length=50)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.group_name


class User(AbstractUser):

    # userGroup = models.ForeignKey(UserGroup, on_delete=models.CASCADE, default=UserGroup.objects.get_or_create(name='Free'))

    def update_grades_for_outdated_tasks(self):
        outdated_tests = Test.objects.filter(end_date__lt=timezone.now()).exclude(
            pk__in=self.testresult_set.all().values('test'))

        for test in outdated_tests:
            TestResult(student=self, test=test, date=timezone.now(), result=0).save()

    def get_grades(self):
        self.update_grades_for_outdated_tasks()

        ret = dict({'grades': list(
            map(lambda el: {'grade': score_to_grade(el.get_score()), 'name': 'Тест - {}'.format(el.test.name),
                            'date': el.date, 'pk': el.pk}, self.testresult_set.all()))})

        grades_list = [el['grade'] for el in ret['grades']]
        ret['avarage_grade'] = str(round(sum(grades_list) / len(grades_list), 2))

        return ret


class QuestionOption(models.Model):
    option_name = models.CharField(max_length=512)
    is_answer = models.BooleanField()

    def __str__(self):
        return self.option_name


class Question(models.Model):
    question_name = models.CharField(max_length=128, default="")
    question = models.TextField(max_length=1024, default="")
    multiple_answers = models.BooleanField(default=False)
    options = models.ManyToManyField(QuestionOption)

    def __str__(self):
        return self.question


class Papa(models.Model):
    papa = models.CharField(max_length=234)
    mama = models.FileField()

    class Meta:
        verbose_name = "Папа"
        verbose_name_plural = "Папы"

    def __str__(self):
        return self.papa


### Subject

class Subject(models.Model):
    name = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.name


### Unit content models

class Lecture(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.name


class Reference(models.Model):
    name = models.CharField(max_length=256, default="")
    reference = models.TextField(default="")

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=256, default="")
    file = models.FileField(upload_to="lecture_files/")

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(max_length=1024, default="")

    questions = models.ManyToManyField(Question)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_questions_count(self):
        return self.questions.count()


class TestResult(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    result = models.FloatField(default=0)

    def set_result_from_score(self, score):
        self.result = score * self.test.get_questions_count() / 100

    def get_score(self):
        return int(self.result / self.test.get_questions_count() * 100)

    def get_grade(self):
        return score_to_grade(self.get_score())


class Task(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


### Unit model

class Unit(models.Model):
    name = models.CharField(max_length=256, default="")

    subject = models.ForeignKey(Subject, models.CASCADE)

    lectures = models.ManyToManyField(Lecture)
    references = models.ManyToManyField(Reference)
    files = models.ManyToManyField(File)
    tests = models.ManyToManyField(Test)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name

### Test model
