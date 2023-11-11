from django.views.generic import View
from django.shortcuts import render, redirect
from main.forms import AddGroupUserForm


class AddGroupUserView(View):

    def get(self, request):
        return render(request, template_name="admin/add_group_user.html", context={'form': AddGroupUserForm()})

    def post(self, request):
        form = AddGroupUserForm(request.POST)

        if not form.is_valid():
            return render(request, template_name="admin/add_group_user.html", context={'form': form})

        form.save()


        if 'continueButton' in request.POST:
            return redirect('add_group_user')
        return redirect('index')
