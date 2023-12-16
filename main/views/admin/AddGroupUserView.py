from django.views.generic import View
from django.shortcuts import render, redirect
from main.forms import AddGroupUserForm


class AddGroupUserView(View):

    def get(self, request):
        is_staff = request.user.is_staff
        is_tutor = request.user.is_tutor
        form = AddGroupUserForm(is_staff=is_staff, is_tutor=is_tutor)
        return render(request, template_name="admin/add_group_user.html", context={'form': form})

    def post(self, request):
        is_staff = request.user.is_staff
        is_tutor = request.user.is_tutor
        form = AddGroupUserForm(request.POST, is_staff=is_staff, is_tutor=is_tutor)

        if not form.is_valid():
            return render(request, template_name="admin/add_group_user.html", context={'form': form})

        form.save()

        if 'continueButton' in request.POST:
            return redirect('add_group_user')

        return redirect('index')
