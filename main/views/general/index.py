from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


# @login_required(login_url='/login/', redirect_field_name=None)
class Index(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = None

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        ...