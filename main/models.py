import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.postgres.fields import ArrayField
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
    name = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class TutorGroup(models.Model):
    name = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class AdminGroup(models.Model):
    name = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class RegistrationLinks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    group_name = models.CharField(max_length=50, unique=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.group_name


class User(AbstractUser):
    is_tutor = models.BooleanField(default=False)

    def update_grades_for_outdated_tasks(self):
        now = timezone.localtime(timezone.now())
        outdated_tests = Test.objects.filter(end_date__lt=now).exclude(
            pk__in=self.testresult_set.all().values('test'))

        for test in outdated_tests:
            TestResult(student=self, test=test, date=now, result=0).save()

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


class Subject(models.Model):
    name = models.CharField(max_length=256, default="")
    tutor_id = models.ForeignKey('User', on_delete=models.PROTECT, null=True)
    enrolled_groups_id = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.name


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

    result = models.IntegerField(default=0)

    def set_result_from_score(self, score):
        self.result = score * self.test.get_questions_count() / 100

    def get_score(self):
        return int(self.result / self.test.get_questions_count() * 100)

    def get_grade(self):
        return score_to_grade(self.get_score())


class StudentFile(models.Model):
    creator = models.IntegerField()
    task_id = models.IntegerField()
    file = models.FileField(upload_to="student_files/")


class Task(models.Model):
    name = models.CharField(max_length=256, default="")
    description = models.TextField(default="")

    start_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    end_date = models.DateTimeField(default=timezone.localtime(timezone.now()))

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=256, default="")

    subject = models.ForeignKey(Subject, models.CASCADE)

    lectures = models.ManyToManyField(Lecture, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    files = models.ManyToManyField(File, blank=True)
    tests = models.ManyToManyField(Test, blank=True)
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.name


class UserTask(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    last_name = models.CharField(max_length=256, null=True) #
    first_name = models.CharField(max_length=256, null=True) #
    group_id = models.ForeignKey('StudentGroup', on_delete=models.PROTECT, null=True) #
    main_task_id = models.ForeignKey('Task', on_delete=models.PROTECT)

    grade = models.IntegerField(null=True, blank=True, default=0)
    own_grade = models.IntegerField(null=True, blank=True, default=0)
    checker_grade = models.IntegerField(null=True, blank=True, default=0)

    time_delivery = models.DateTimeField(auto_now_add=True)




class GroupCheck(models.Model):
    usser_id = models.ForeignKey('User', on_delete=models.PROTECT)
    group_check = models.IntegerField(null=True)
    main_task_id = models.ForeignKey('Task', on_delete=models.PROTECT)
    user_check_id = models.JSONField(default=list, blank=True, null=True)


class Notification(models.Model):
    header = models.CharField(max_length=40)
    body = models.CharField(max_length=128)
    is_checked = models.BooleanField(default=False)
    time_delivery = models.DateTimeField(default=timezone.localtime(timezone.now()))
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)


    def __str__(self):
        return str(self.user_id)
      
