from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import StudentGroup


class StudentGroupRequiredMixin(UserGroupRequiredMixin):

    def getGroupsList(self):
        return list(StudentGroup.objects.all())
