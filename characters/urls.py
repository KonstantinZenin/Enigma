from django.urls import path
from .views import (
    CharacterCreateView, CharacterUpdateView, 
    CharacterDetailView, CharacterListView, 
    UserCharacterListView
)

app_name = 'characters'

urlpatterns = [
    path('create/', CharacterCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', CharacterUpdateView.as_view(), name='edit'),
    path('<int:pk>/', CharacterDetailView.as_view(), name='detail'),
    path('', CharacterListView.as_view(), name='list'),
    path('user/<int:pk>/', UserCharacterListView.as_view(), name='user_list'),
]
