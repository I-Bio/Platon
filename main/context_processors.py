from .models import Subject, Unit, Notification


def global_models(request):

    try:
        subjects_all = Subject.objects.all()
        if request.user.is_tutor:
            tutor_id = request.user.pk

            subjects_list = []
            for subject in subjects_all:
                if tutor_id == subject.tutor_id.pk:
                    subjects_list.append(subject)
            subjects_all = subjects_list
        else:
            group = request.user.groups.all().first().pk

            subjects_list = []
            for subject in subjects_all:
                if group in subject.enrolled_groups_id:
                    subjects_list.append(subject)
            subjects_all = subjects_list
    except:
        subjects_all = None

    return {'subjects_all': subjects_all}


def last_notification(request):
    notification = Notification.objects.filter(user_id=request.user.pk).order_by('-time_delivery')
    new_notification = Notification.objects.filter(user_id=request.user.pk, is_checked=False).count()
    return {'notifications': notification, 'new_notifications': new_notification}
