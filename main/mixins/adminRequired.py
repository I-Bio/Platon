from main.mixins.userGroupRequired import UserGroupRequiredMixin
from main.models import AdminGroup


class AdminRequiredMixin(UserGroupRequiredMixin):
    login_url = '/login'
    userGroup = 'list(AdminGroup.objects.all())'