from django import template
from main.models import User

register = template.Library()

@register.filter
def get_user(user_id):
    user = User.objects.get(id=user_id)
    return f"{user.first_name} {user.last_name}"