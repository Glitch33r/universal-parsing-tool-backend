from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import bot_list_view, bot_create_view, bot_delete, bot_update

app_name = 'bot'
urlpatterns = [
    path('list/', bot_list_view, name='bot-list'),  
    path('create/', bot_create_view, name='bot-create'),
    # path('<int:id>/', views.login, name='bot-detail'),
    path('update/<int:pk>', bot_update, name='bot-update'),
    path('delete/<int:obj_id>', bot_delete, name='bot-delete'),
]
