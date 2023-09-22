from django import template
from ..models import ChatMessage
from django.db.models import Q

register = template.Library()

@register.filter
def get_last_message(friend):
    last_message = ChatMessage.objects.filter(
        Q(msgsender=friend.profile)
        | Q(msgreciver=friend.profile)
    ).order_by('-sent_at').first()
    return last_message.body if last_message else None

@register.filter
def check_for_seen(friend):
    last_message = ChatMessage.objects.filter(
        Q(msgsender=friend.profile)
        | Q(msgreciver=friend.profile)
    ).order_by('-sent_at').first()
    if last_message:
        if (last_message.seen == False and last_message.msgsender == friend.profile):
            return False
        else:
            return True
    