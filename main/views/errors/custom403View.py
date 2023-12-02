from django.views import View
from django.shortcuts import render


class Custom403View(View):
    def get(self, request, exception):
        return render(request, 'errors/errors.html', {'error_code': 403, 'error_description': ' Доступ запрещен. ',
                                                      'error_message': ' У вас нет доступа к этой странице. '},
                      status=403)
