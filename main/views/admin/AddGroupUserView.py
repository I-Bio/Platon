from django.views.generic import FormView
from main.forms import AddGroupUserForm


class AddGroupUserView(FormView):
    form_class = AddGroupUserForm
    template_name = 'admin/add_group_user.html'
    success_url = '/done'

    def form_valid(self, form):
        form.save()
        return super(AddGroupUserView, self).form_valid(form)
