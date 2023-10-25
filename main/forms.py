from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from Platon import settings
from .models import StudentGroup, TeacherGroup, AdminGroup
from django.contrib.auth.models import Group, Permission


### Auth forms

class LoginForm(forms.Form):
    email = forms.EmailField(min_length=3, initial="")
    password = forms.CharField(min_length=8, max_length=32, initial="")


class RegistrationForm(forms.Form):
    first_name = forms.CharField(min_length=3, max_length=32, initial="")
    last_name = forms.CharField(min_length=3, max_length=32, initial="")

    email = forms.EmailField(min_length=3, initial="")

    group = forms.ModelChoiceField(queryset=models.StudentGroup.objects.all(), to_field_name="name", empty_label=None)

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
        fields = ['name']


class UnitForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=models.Subject.objects, empty_label=None)

    class Meta:
        model = models.Unit
        fields = ['name', 'subject']


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


class AddGroupUserForm(forms.Form):
    student = 'Student'
    teacher = 'Teacher'
    admin = 'Admin'

    user_choices = [
        (student, 'Студент'),
        (teacher, 'Преподаватель'),
        (admin, 'Администратор'),
    ]

    user_type = forms.ChoiceField(choices=user_choices)
    name = forms.CharField(max_length=50)

    model_mapping = {
        student: StudentGroup,
        teacher: TeacherGroup,
        admin: AdminGroup,
    }

    def save(self):
        user_type = self.cleaned_data['user_type']
        name = self.cleaned_data['name']
        key = ...

        model_class = self.model_mapping.get(user_type)
        if model_class:
            model_class.objects.create(name=name)

            group = Group.objects.create(name=name)
            permissions = Permission.objects.none()
            group.permissions.set(permissions)
