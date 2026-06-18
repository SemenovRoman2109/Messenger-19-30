from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils.friends import get_friends_by_section
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .utils.friends_actions import *
from profile_app.models import *

# Create your views here.
class AuthView(TemplateView):
    template_name = 'user_app/auth.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form_register'] = RegistrationForm()
        context['form_login'] = EmailAuthenticationForm(request=self.request)
        context['form_confirm_email'] = ""
        return context
        
class RegisterView(View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user = user)
            return JsonResponse(data={
                "success": True
            })
            
        return JsonResponse(data={
            "success": False,
            "errors": form.errors.get_json_data()
        })
    
# form.errors.get_json_data() - отримує всі помилки з форми 

class LoginView(View):
    def post(self, request):
        form = EmailAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request = request, user = form.get_user())
            
            return JsonResponse(data={
                "success": True
            })
            
        return JsonResponse(data={
            "success": False,
            "errors": form.errors.get_json_data()
        })

class FriendsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/friends.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sections'] = {
            'requests': {"title" : 'Запити', "users": get_friends_by_section(current_user = self.request.user, section = "requests")[:6]},
            'recommendations': {"title" : 'Рекомендації', "users": get_friends_by_section(current_user = self.request.user, section = "recommendations")[:6]},
            'friends': {"title" : 'Друзі', "users": get_friends_by_section(current_user = self.request.user, section = "friends")[:6]},
        }
        
        return context
    
class FriendsSectionView(LoginRequiredMixin, View):
    def get(self, request, section):
        users = get_friends_by_section(current_user=request.user, section = section)
        page_num = request.GET.get('page')
        page = Paginator(users, 15).get_page(page_num)
        html = render_to_string(
            'user_app/particles/friends/friend_cards.html',
            {'users': page.object_list, 
             'section': section}
        )
        return JsonResponse({'html': html, "has_next": page.has_next()})

class FriendsActionView(LoginRequiredMixin, View):
    def post(self, request, action, user_id):
        other_user = User.objects.get(id = user_id)
        user = request.user

        if action == "add":
            return JsonResponse(add_friend_request(user, other_user))
        elif action == 'delete':
            return JsonResponse(delete_friendship(user, other_user))
        elif action == 'ignore':
            return JsonResponse(ignore_friendship(user, other_user))
        elif action == 'accept':
            data = accept_friend_request(user, other_user)
            data['friend_html'] = render_to_string(
                'user_app/particles/friends/friend_cards.html',
                {'users': [other_user], 'section': 'friends'}
            )
            return JsonResponse(data)
        

