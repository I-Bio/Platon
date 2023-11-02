from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from Platon import settings
from .models import StudentGroup, User


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
            cleaned_data['options'] = list(zip(self.data.getlist('option_text[]'), map(lambda el: bool(int(el)), self.data.getlist('option_answer[]'))))

        if 'question_type' in self.data:
            cleaned_data['question_type'] = bool(int(self.data['question_type']))

        return cleaned_data

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)

        question.save()

        for option in question.options.all():
            option.delete()

        for text, is_answer in self.cleaned_data['options']:
            option = models.QuestionOption(option_name = text, is_answer = is_answer)
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
            question = models.Question.objects.filter(pk = question_pk)

            if question.exists():
                question = question.first()
                test.questions.add(question)

        test.save()

        return test

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['name', 'description', 'start_date', 'end_date']



class UserTaskForm(forms.ModelForm):
    class Meta:
        model = models.UserTask
        fileds = ['grade']
        exclude = ['name_task', 'user_id', 'last_name', 'first_name', 'group_id', 'main_task_id', 'time_delivery']