from django.urls import path
from .views import redirect_to_steam, steam_callback, get_current_user

urlpatterns = [
    path('steam/', redirect_to_steam, name='steam_login'),
    path('steam/callback/', steam_callback, name='steam-callback'),
    path('user/', get_current_user, name='current-user'),
]