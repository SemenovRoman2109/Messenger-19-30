from django.urls import path 
from .views import *

urlpatterns = [
    path('', AuthView.as_view(), name = "auth"),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('friends/', FriendsView.as_view(), name = 'friends'),
    path('friends/<str:section>/', FriendsSectionView.as_view(), name = 'friends_section'),
    path('friends/<str:action>/<int:user_id>/', FriendsActionView.as_view(), name = 'friends_actions')
]

