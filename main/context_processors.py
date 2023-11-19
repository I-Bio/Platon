from .models import Subject, Unit, Notification


def global_models(request):
    return {'subjects_all': Subject.objects.all(), 'units_all': Unit.objects.all()}


def last_notification(request):
    notification = Notification.objects.filter(user_id=request.user.pk).order_by('-time_delivery')
    new_notification = Notification.objects.filter(user_id=request.user.pk, is_checked=False).count()
    return {'notifications': notification, 'new_notifications': new_notification}
