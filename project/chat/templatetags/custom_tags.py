from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return User.objects.get(pk=u.pk)
    return None