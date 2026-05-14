from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils.friends import get_friends_by_section
from django.core.paginator import Paginator
from django.template.loader import render_to_string


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
            form.save()
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
    
class FriendsSectionView(View):
    def get(self, request, section):
        users = get_friends_by_section(current_user=request.user, section = section)
        page_num = request.GET.get('page')
        page = Paginator(users, 10).get_page(page_num)
        html = render_to_string(
            'user_app/particles/friends/friend_cards.html',
            {'users': page.object_list, 
             'section': section}
        )
        return JsonResponse({'html': html, "has_next": page.has_next()})
        
# LoginRequiredMixin - клас потрібно успадковувати, щоб на сторінку могли зайти лише авторизовані (імпортувати з django.contrib.auth.mixins)