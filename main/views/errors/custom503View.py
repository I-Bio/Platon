from django.views import View
from django.shortcuts import render


class Custom503View(View):
    def get(self, request, exception):
        return render(request, 'errors/errors.html',
                      {'error_code': 404, 'error_description': ' Сервис временно недоступен ',
                       'error_message': ' Сервер не может обработать ваш запрос в данный момент '}, status=503)
