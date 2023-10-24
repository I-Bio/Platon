from django.views.generic import FormView
from main.forms import AddGroupUser


class AddGroupUser(FormView):
    form_class = AddGroupUser
    template_name = 'admin/add_group_user.html'
    success_url = '/done'

    def form_valid(self, form):
        form.save()
        return super(AddGroupUser, self).form_valid(form)
