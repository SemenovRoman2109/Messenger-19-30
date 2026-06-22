from django.urls import path 
from .views import *

urlpatterns = [
    path('settings/', SettingsView.as_view(), name = "settings"),
    path('update_profile/', UpdateProfileView.as_view(), name = "update_profile"),
    path('update_info/', UpdateInfoView.as_view(), name = "update_info"),
]