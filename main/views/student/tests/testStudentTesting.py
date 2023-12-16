from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from main.models import Unit, TestResult, Test


class TestStudentTesting(StudentGroupRequiredMixin, View):
    def get(self, request, unit_id, test_id):
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        unit = unit.first()

        subject = unit.subject

        if (request.user.groups.first().pk in subject.enrolled_groups_id) == False:
            raise PermissionDenied()

        test = Test.objects.filter(pk=test_id)

        if not test.exists():
            return redirect('index')

        test = test.first()

        if TestResult.objects.filter(student=request.user, test=test).exists():
            return redirect('test_result', unit_id, test_id)

        now = timezone.localtime(timezone.now())

        if test.start_date > now or test.end_date < now + timezone.timedelta(minutes=2):
            return redirect('unit_content', unit_id)

        return render(request, "content_bank/test/testing.html", {'test': test})

    def post(self, request, unit_id, test_id):
        test = Test.objects.filter(pk=test_id).first()
        score = 0.0

        for question in test.questions.all():
            key = 'answer-{}[]'.format(question.pk)

            if not key in request.POST:
                continue

            user_answers = list(map(lambda el: int(el), request.POST.getlist(key)))

            if question.multiple_answers:
                answer_options = question.options.filter(is_answer=True)

                local_score = 0
                score_per_answer = 1 / len(answer_options)
                answers_id = list(map(lambda el: el['pk'], answer_options.values('pk')))
                for user_answer in user_answers:
                    if user_answer in answers_id:
                        local_score += score_per_answer
                    else:
                        local_score -= score_per_answer

                score += max(local_score, 0)
            else:
                if len(user_answers) == 1:
                    answer_option = question.options.filter(is_answer=True)

                    if answer_option.exists():
                        if answer_option.first().pk == user_answers[0]:
                            score += 1

        TestResult(student=request.user, test=test, result=score).save()

        return redirect('test_result', unit_id, test_id)
