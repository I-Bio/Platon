from django.views import View
from django.shortcuts import render


class Custom404View(View):
    def get(self, request, exception):
        return render(request, 'errors/errors.html',
                      {'error_code': 404, 'error_description': ' Упс. Страничка не найдена.',
                       'error_message': ' Мы не можем найти страничку, которую вы ищите. '}, status=404)
