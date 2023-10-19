from django.shortcuts import render
from django.views import View


# @login_required(login_url='/login/', redirect_field_name=None)
class Index(View):

    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        ...