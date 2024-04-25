from django.shortcuts import render
from django.views import View

from main.mixins.tutorRequired import TutorRequiredMixin
from main.models import Subject, GroupCheck


class ShowReviewView(TutorRequiredMixin, View):
    def get(self, request):
        subjects_of_this_teacher = Subject.objects.filter(tutor_id=request.user.id).first()
        review = GroupCheck.objects.filter(main_task_id__unit__subject=subjects_of_this_teacher)

        return render(request, "tutor/showReview.html",
                      {"review": review})

    def post(self, request):
        if 'subjects_of_this_teacher' in request.POST:
            subjects_of_this_teacher_id = int(request.POST['subjects_of_this_teacher'])
            subjects_of_this_teacher = Subject.objects.get(pk=subjects_of_this_teacher_id)
            review = GroupCheck.objects.filter(main_task_id__unit__subject=subjects_of_this_teacher)

            print(review)

            return render(request, "tutor/showReview.html",
                          {'review': review, 'subjects_of_this_teacher': subjects_of_this_teacher})
