from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

app_name = 'accounts'
urlpatterns = [
    path('log-in/', views.login, name='log-in'),
    path('log-out/', views.logout, name='log-out'),
    path('settings/', views.settings, name='settings'),
]
