from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GuildMember, Role

class GuildMemberAdmin(UserAdmin):
    model = GuildMember
    list_display = ('username', 'email', 'name', 'surname', 'role')
    
    # Добавляем кастомные поля к стандартным
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Guild Member Info', {'fields': ('name', 'surname', 'patronymic', 'birth_date', 'phone_number', 'avatar', 'telegram_username', 'vk_id', 'address', 'role')})
    )

admin.site.register(GuildMember, GuildMemberAdmin)
admin.site.register(Role)
