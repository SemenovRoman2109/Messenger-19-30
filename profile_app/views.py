from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View

# Create your views here.
class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_app/settings.html'
    
class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.username = request.POST.get("username")
        request.user.profile.avatar = request.FILES.get("file")
        
        request.user.save()
        request.user.profile.save()
        return redirect("settings")
    
class UpdateInfoView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.email = request.POST.get("email")
        request.user.last_name = request.POST.get("last-name")
        request.user.first_name = request.POST.get("first-name")
        request.user.profile.birth_date = request.POST.get("date")
        
        request.user.save()
        request.user.profile.save()
        return redirect("settings")