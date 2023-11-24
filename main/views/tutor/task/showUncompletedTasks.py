from django.views import View


class showUncompletedTasks(View):
    def get(self, request, task_id, group_id):

        ...