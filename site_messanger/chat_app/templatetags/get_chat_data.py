from django import template
from ..models import Chat

register = template.Library()

@register.simple_tag
def get_unreaded_messages(chat_id, user):
    chat = Chat.objects.filter(id = chat_id).first()
    if chat:
        unreaded_messages = chat.messages.exclude(readers = user).exclude(sender = user)
        return unreaded_messages.count()
    
