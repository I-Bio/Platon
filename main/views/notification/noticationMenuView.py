from django.shortcuts import render
from django.views import View

from main.models import Notification


class NotificationMenuView(View):
    def get(self, request):
        Notification.objects.filter(user_id=request.user.pk).update(is_checked=True)
        notification = Notification.objects.filter(user_id=request.user.pk).order_by('-time_delivery')
        return render(request, template_name="notification/notificationMenu.html",
                      context={'notifications': notification})
