from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import *

app_name = 'bot'
urlpatterns = [
    path('doc/functional', bot_function_docs, name='func-docs'),
    path('list/', bot_list_view, name='bot-list'),  
    path('list/code', bot_code_list_view, name='bot-code-list'),
    path('create/', bot_create_view, name='bot-create'),
    path('update/<int:pk>', bot_update_view, name='bot-update'),
    path('delete/<int:obj_id>', bot_delete_view, name='bot-delete'),
    path('run/<int:pk>', run_bot, name='bot-run'),
    path('log/list', log_list, name='bot-log'),
    path('data/list', bot_data, name='bot-data'),
]
