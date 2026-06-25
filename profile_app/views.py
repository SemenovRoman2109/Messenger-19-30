from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.views import PasswordChangeView

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
    
class UpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        password_old = request.POST.get("old-password")
        password_new = request.POST.get("new-password")
        password_confirm = request.POST.get("confirm-password")

        if password_old and password_new and password_confirm:
            if request.user.check_password(password_old):
                if password_new == password_confirm:
                    request.user.set_password(password_new)
                    request.user.save()
                    update_session_auth_hash(request = request, user = request.user)

        # user.check_password(пароль) - перевіряє чи правильний пароль
        # user.set_password(пароль) - задає новий пароль
        # update_session_auth_hash(request, user) - оновлює сесію користувача ( щоб не вибило з акаунту після зміни паролю )

        return redirect("settings")
        
        
class UpdateSignatureView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        request.user.profile.pseudonym = request.POST.get("pseudonym")
        request.user.profile.is_text_signature = request.POST.get("is_text_signature") == "on"
        
        file = request.FILES.get("signature")
        if file:
            request.user.profile.signature = file
        request.user.profile.is_image_signature = request.POST.get("is_image_signature") == "on"
        
        request.user.profile.save()
        return redirect("settings")