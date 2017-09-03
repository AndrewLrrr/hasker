from datetime import timedelta

from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()


@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, unicode):
        return text.startswith(starts)
    return False


@register.filter(name='get_human_date')
def get_human_date(date):
    now = timezone.now()
    difference = now - date
    if difference <= timedelta(minutes=10):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(date).split(', ')[0]}
