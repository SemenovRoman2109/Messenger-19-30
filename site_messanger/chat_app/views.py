from django.shortcuts import render
from django.views.generic import TemplateView , View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, User, Message, MessageImage
from user_app.utils.friends import get_friends_by_section
from django.http import JsonResponse
from django.core.paginator import Paginator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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

        context["group_chats"] = Chat.objects.filter(is_group = True, users = self.request.user)

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


class GetMessagesView(LoginRequiredMixin, View):
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.filter(id = chat_id, users = request.user).first()
        if chat:
            page_number = request.GET.get("page")
            messages = chat.messages.order_by('-created_at')
            paginator = Paginator(messages, 20)
            message_list = paginator.get_page(page_number)
            if int(page_number) > paginator.num_pages:
                return JsonResponse({"success" : False})
            else:
                message_data_list = []
                for message in message_list:
                    list_url_image = []
                    for image in message.images.all():
                        list_url_image.append(image.image.url)
                        
                    message_data_list.append({
                        'sender': message.sender.email,
                        'text': message.text,
                        'date': message.created_at.date(),
                        'time': str(message.created_at.timetuple().tm_hour) + ":" + str(message.created_at.timetuple().tm_min),
                        'images': list_url_image
                    })
                return JsonResponse({
                    "success" : True,
                    "messages": message_data_list
                })
                
class CreateGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        
        new_chat = Chat.objects.create(
            is_group = True, 
            admin = request.user, 
            name = data.get('name'), 
        )
        new_chat.users.add(request.user)
        
        user_friends = get_friends_by_section(current_user= request.user, section= 'friends')
        for user_id in data.get('friends'):
            user = User.objects.filter(id = user_id).first()
            if user in user_friends:
                new_chat.users.add(user)
                
        return JsonResponse({
            'success': True,
            'name': new_chat.name,
            'chat_id':new_chat.id
        })
        
class CreateMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        print(request.POST, request.FILES)
        chat_id = request.POST.get("chat_id")
        chat = Chat.objects.filter(id = chat_id, users = request.user).first()
        if chat:
            new_message = Message.objects.create(
                text = request.POST.get("text"), 
                chat_id=chat.id, 
                sender=request.user
            )
            list_url_image = []
            for image in request.FILES.getlist('image'):
                new_image = MessageImage.objects.create(
                    image = image,
                    message = new_message 
                )
                list_url_image.append(new_image.image.url)
            
            channel_layer = get_channel_layer()
            
            async_to_sync(channel_layer.group_send)(
                f"chat_{chat.id}", 
                {
                    "type": "send_message",
                    "message": {
                        'sender': new_message.sender.email,
                        'text': new_message.text,
                        'date': str(new_message.created_at.date()),
                        'time': str(new_message.created_at.timetuple().tm_hour) + ":" + str(new_message.created_at.timetuple().tm_min),
                        'images': list_url_image
                    },
                }
            )
            
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})