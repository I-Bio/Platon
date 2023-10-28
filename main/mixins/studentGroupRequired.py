from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import StudentGroup


class StudentGroupRequiredMixin(UserGroupRequiredMixin):
    login_url = '/login'
    userGroup = StudentGroup.objects.all()
