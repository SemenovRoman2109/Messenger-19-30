from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class AuthView(TemplateView):
    template_name = 'user_app/auth.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['form_register'] = ""
        context['form_login'] = ""
        context['form_confirm_email'] = ""
        return context
