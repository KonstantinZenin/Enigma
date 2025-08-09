from django.urls import path
from . import views

app_name = 'communications'  # Добавляем пространство имён

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
]
