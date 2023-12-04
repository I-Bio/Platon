from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse


class UserGroupRequiredMixin(AccessMixin):
    login_url = '/login'
    redirect_field_name = None

    def getGroupsList(self):
        ...

    def hasExistGroup(self):
        resultString = self.request.user.groups.filter(name=self.getGroupsList()).exists()
        resultList = self.request.user.groups.filter(name__in=self.getGroupsList()).exists()
        result = resultString or resultList
        return result

    def dispatch(self, request, *args, **kwargs):
        perms = self.hasExistGroup()

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_staff:
            perms = True

        if not perms:
            return HttpResponse(status=403)

        return super().dispatch(request, *args, **kwargs)
