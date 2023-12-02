from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from main.models import Unit, Lecture, Reference, File, Test, Task, Subject


# @login_required(login_url='/login/', redirect_field_name=None)
class UnitContent(View):
    def get(self, request, unit_id):
        print(request.user.pk)
        unit = Unit.objects.filter(pk=unit_id)

        if not unit.exists():
            return redirect('index')

        unit = unit.first()

        # print('привет', unit.subject.users_id)
        flag_stud = False
        flag_tutor = False



        if request.user.pk == unit.subject.tutor_id.pk:
            flag_tutor = True

        if request.user.pk in unit.subject.users_id:
            flag_stud = True
        else:
            return HttpResponse("Вы не зачислены на курс")

        context = {
            'unit': unit,
            'flag_tutor' : flag_tutor,
            'flag_stud' : flag_stud,
                   }
        return render(request, "content_bank/unit/content.html", context=context)

    def post(self, request, unit_id):
        unit = Unit.objects.filter(pk=unit_id).first()

        if 'toDelete' in request.POST:

            type, id = request.POST['toDelete'].split('-')

            models_dict = dict({'lecture': Lecture,
                                'reference': Reference,
                                'file': File,
                                'test': Test,
                                'task': Task})

            if not type in models_dict:
                return HttpResponse(status=400)

            content = models_dict[type].objects.filter(pk=id)

            if not content.exists():
                return HttpResponse(status=400)

            content = content.first()

            getattr(unit, type + 's').remove(content)

            content.delete()

        return HttpResponse(status=200)