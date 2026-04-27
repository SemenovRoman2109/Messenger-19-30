from django.urls import path 
from .views import AuthView, RegisterView, LoginView

urlpatterns = [
    path('', AuthView.as_view(), name = "auth"),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login')
]