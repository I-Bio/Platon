from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import AdminGroup


class AdminRequiredMixin(UserGroupRequiredMixin):

    def getGroupsList(self):
        return list(AdminGroup.objects.all())
