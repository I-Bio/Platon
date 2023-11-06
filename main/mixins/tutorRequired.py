from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import TutorGroup


class TutorRequiredMixin(UserGroupRequiredMixin):
    login_url = '/login'
    userGroup = list(TutorGroup.objects.all())


