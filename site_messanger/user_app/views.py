from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import login

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