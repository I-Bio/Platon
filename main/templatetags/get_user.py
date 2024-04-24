from django import template
from main.models import User, GroupCheck, Subject, Unit

register = template.Library()


@register.filter
def get_user(user_id):
    user = User.objects.get(id=user_id)
    return f"{user.first_name} {user.last_name}"


@register.filter
def get_subject(main_task_id):
    unit = Unit.objects.get(tasks=main_task_id)

    subject = Subject.objects.filter(unit=unit).first()

    return int(subject.pk)

@register.filter
def get_unit(main_task_id):

    return int(main_task_id.pk)
