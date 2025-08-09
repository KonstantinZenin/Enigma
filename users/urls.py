from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('generate-invite/', views.generate_invite_view, name='generate_invite'),
    path('invite-form/', views.invite_code_form_view, name='invite_form'),
    path('invite-error/', views.invite_error_view, name='invite_error'),
]
