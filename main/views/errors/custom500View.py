from django.views import View
from django.shortcuts import render


class Custom500View(View):
    def get(self, request, *args, **argv):
        return render(request, 'errors/errors.html',
                      {'error_code': 500, 'error_description': ' Сервис временно недоступен ',
                       'error_message': ' Сервер не может обработать ваш запрос в данный момент '}, status=500)
