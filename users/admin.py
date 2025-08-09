from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GuildMember, InviteCode

class GuildMemberAdmin(UserAdmin):
    model = GuildMember
    list_display = ('username', 'name', 'surname', 'telegram_username')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'patronymic', 'birth_date', 'phone_number', 'avatar', 'telegram_username', 'vk_id', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        # ('Guild Info', {'fields': ('role',)}),  # Удалено, так как поле role больше не существует
    )

admin.site.register(GuildMember, GuildMemberAdmin)
admin.site.register(InviteCode)
