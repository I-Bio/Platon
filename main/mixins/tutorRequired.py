from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import TutorGroup


class TutorRequiredMixin(UserGroupRequiredMixin):

    def getGroupsList(self):
        return list(TutorGroup.objects.all())