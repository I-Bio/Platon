from django.views.generic import TemplateView


class DoneView(TemplateView):
    template_name = 'admin/done.html'
