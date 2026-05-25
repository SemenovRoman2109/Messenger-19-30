from django.shortcuts import render
from django.views.generic import TemplateView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, User
from user_app.utils.friends import get_friends_by_section
from django.http import JsonResponse
import json
# Create your views here.

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat_app/chat.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chats = Chat.objects.filter(is_group = False, users = self.request.user)
        data = []
        for chat in chats:
            other_user = chat.users.exclude(id = self.request.user.id).first()
            data.append({
                "chat_id": chat.id,
                "other_user":  other_user
            })
        context["individual_chats"] = data

        context["friends"] = get_friends_by_section(current_user = self.request.user, section = "friends")
        return context

class CreateChatView(LoginRequiredMixin, View): 
    def post(self, request):
        data = json.loads(request.body)
        friend_id = data.get('friend_id')
        friend = User.objects.filter(id = friend_id).first()

        chat = Chat.objects.filter(is_group = False, users = friend).filter(users = request.user).first()
        is_new_chat = False
        if not chat: 
            chat = Chat.objects.create(is_group = False )
            chat.users.set([request.user, friend])
            is_new_chat = True  
        print(chat)
        return JsonResponse({ "chat_id" : chat.id, "friend_email" : friend.email, 'is_new': is_new_chat})
