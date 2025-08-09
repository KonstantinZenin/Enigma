from django.urls import path
from . import views

app_name = 'event_calendar'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/join/', views.EventJoinView.as_view(), name='event_join'),
    path('<int:pk>/leave/', views.EventLeaveView.as_view(), name='event_leave'),
    path('calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
    path('events.json', views.EventJsonView.as_view(), name='event_json'),
]
