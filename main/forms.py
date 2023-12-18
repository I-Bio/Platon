from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from Platon import settings
from .models import StudentGroup, TutorGroup, AdminGroup, User, RegistrationLinks, Subject
from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


### Auth forms

class LoginForm(forms.Form):
    email = forms.EmailField(min_length=3, initial="")
    password = forms.CharField(min_length=8, max_length=32, initial="")


class RegistrationForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=32, initial="")
    last_name = forms.CharField(min_length=1, max_length=32, initial="")

    email = forms.EmailField(min_length=3, initial="")

    group = forms.CharField(min_length=1, max_length=32, initial="")

    password = forms.CharField(min_length=8, max_length=32, initial="")


### Content forms

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_name', 'question']

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()

        if 'option_text[]' in self.data and 'option_answer[]' in self.data:
            cleaned_data['options'] = list(zip(self.data.getlist('option_text[]'),
                                               map(lambda el: bool(int(el)), self.data.getlist('option_answer[]'))))

        if 'question_type' in self.data:
            cleaned_data['question_type'] = bool(int(self.data['question_type']))

        return cleaned_data

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)

        question.save()

        for option in question.options.all():
            option.delete()

        for text, is_answer in self.cleaned_data['options']:
            option = models.QuestionOption(option_name=text, is_answer=is_answer)
            option.save()
            question.options.add(option)

        question.multiple_answers = self.cleaned_data['question_type']

        question.save()

        return question


class SubjectForm(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = ['name', 'tutor_id']


class UnitForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=models.Subject.objects.none(), empty_label=None)

    class Meta:
        model = models.Unit
        fields = ['name', 'subject']

    def __init__(self, *args, **kwargs):
        tutor_id = kwargs.pop('tutor_id')

        super(UnitForm, self).__init__(*args, **kwargs)

        self.fields['subject'].queryset = Subject.objects.filter(tutor_id=tutor_id)



class LectureForm(forms.ModelForm):
    class Meta:
        model = models.Lecture
        fields = ['name', 'description']


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = models.Reference
        fields = ['name', 'reference']


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = ['name', 'file']


class TestForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS)
    end_date = forms.DateTimeField(input_formats=settings.DATETIME_INPUT_FORMATS)

    class Meta:
        model = models.Test
        fields = ['name', 'description', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super(TestForm, self).clean()

        if 'questions[]' in self.data:
            cleaned_data['questions[]'] = list(map(lambda el: int(el), self.data.getlist('questions[]')))

        return cleaned_data

    def save(self, commit=True):
        test = super(TestForm, self).save(commit=False)

        test.save()

        test.questions.clear()

        for question_pk in self.cleaned_data.get('questions[]'):
            question = models.Question.objects.filter(pk=question_pk)

            if question.exists():
                question = question.first()
                test.questions.add(question)

        test.save()

        return test


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['name', 'description', 'start_date', 'end_date']


class StudentTaskForm(forms.Form):
    files = MultipleFileField()
    own_grade = forms.IntegerField()



class UserTaskForm(forms.ModelForm):
    class Meta:
        model = models.UserTask
        fileds = ['grade']
        exclude = ['name_task', 'user_id', 'last_name', 'first_name', 'group_id', 'main_task_id', 'time_delivery']


class AddGroupUserForm(forms.Form):
    name = forms.CharField(max_length=50)
    user_type = forms.ChoiceField(choices=[])

    def save(self):
        user_type = self.cleaned_data['user_type']
        name = self.cleaned_data['name']

        model_class = self.model_mapping.get(user_type)
        if model_class:
            group = Group.objects.create(name=name)
            permissions = Permission.objects.none()
            group.permissions.set(permissions)

            model_class.objects.create(name=group)

    def __init__(self, *args, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_tutor = kwargs.pop('is_tutor', False)

        self.model_mapping = {}

        super(AddGroupUserForm, self).__init__(*args, **kwargs)

        if is_staff:
            student = 'Student'
            tutor = 'Teacher'
            admin = 'Admin'
            none = 'None'

            user_choices = [
                (none, '---'),
                (student, 'Студенты'),
                (tutor, 'Преподаватели'),
                (admin, 'Администрация'),
            ]

            self.model_mapping = {
                student: StudentGroup,
                tutor: TutorGroup,
                admin: AdminGroup,
            }

            self.fields['user_type'] = forms.ChoiceField(choices=user_choices)

        if is_tutor:
            student = 'Student'
            none = 'None'

            user_choices = [
                (none, '---'),
                (student, 'Студенты'),
            ]

            self.model_mapping = {
                student: StudentGroup,
            }

            self.fields['user_type'] = forms.ChoiceField(choices=user_choices)


class ChooseStudentsToChecker(forms.ModelForm):
    class Meta:
        model = models.GroupCheck
        fields = ['usser_id', 'group_check', 'main_task_id']

    def clean(self):
        cleaned_data = super(ChooseStudentsToChecker, self).clean()

        if 'questions[]' in self.data:
            cleaned_data['questions[]'] = list(map(lambda el: int(el), self.data.getlist('questions[]')))

        return self.cleaned_data


class AddGradeForm(forms.Form):
    grade = forms.IntegerField()

    def save(self, user_task):
        if user_task:
            grade = self.cleaned_data['grade']
            user_task.grade = grade
            user_task.save()


class AddGradeStudentForm(forms.Form):
    grade = forms.IntegerField()

    def save(self, user_task):
        if user_task:
            grade = self.cleaned_data['grade']
            user_task.checker_grade = grade
            user_task.save()


class CreateInviteLinkForm(forms.Form):
    group_name = forms.ModelChoiceField(queryset=StudentGroup.objects.none(), label='')
    end_date = forms.DateTimeField()

    def save(self):
        group_name = self.cleaned_data['group_name']
        end_date = self.cleaned_data['end_date']

        try:
            link = RegistrationLinks.objects.create(group_name=group_name, end_date=end_date)
        except IntegrityError:
            ...

    def __init__(self, *args, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_tutor = kwargs.pop('is_tutor', False)

        super(CreateInviteLinkForm, self).__init__(*args, **kwargs)

        if is_staff:
            all_groups = list(StudentGroup.objects.all()) + list(TutorGroup.objects.all()) + list(
                AdminGroup.objects.all())
            self.fields['group_name'] = forms.ChoiceField(choices=[(group.name, str(group)) for group in all_groups],
                                                          label='Выберите группу')

        if is_tutor:
            self.fields['group_name'].queryset = StudentGroup.objects.all()
            self.fields['group_name'].empty_label = None
            self.fields['group_name'].label = 'Выберите группу'


class IdSelector(forms.Form):
    id = forms.IntegerField()


class AdderToTheCourceForm(forms.Form):
    subjects_of_this_teacher = forms.IntegerField()
    enrolled_student_group = forms.JSONField(required=False)

    def save(self, selected_group):
        subjects_of_this_teacher = self.cleaned_data['subjects_of_this_teacher']
        enrolled_student_group_values = selected_group

        subject = Subject.objects.filter(pk=subjects_of_this_teacher).update(enrolled_groups_id=enrolled_student_group_values)
