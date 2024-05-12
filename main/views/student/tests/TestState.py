from main.mixins.studentGroupRequired import StudentGroupRequiredMixin
from django.views import View
from django.shortcuts import redirect, render


from main.models import Test, TestResult



class TestState(View, StudentGroupRequiredMixin):
    def get(self, request):

        test = Test.objects.filter(name = str(request.user))

        if not test.exists():
            return redirect('index')

        test = test.first()

        if TestResult.objects.filter(student=request.user, test=test).exists():
            return redirect('test_state_result')

        return render(request, "students/TestState.html", {'test': test})


    def post (self, request):
        test = Test.objects.filter(name=request.user).first()
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

        return redirect('test_state_result')