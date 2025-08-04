from django.contrib import admin
from .models import GameCharacter

@admin.register(GameCharacter)
class GameCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'character_class', 'race', 'role', 'server', 'user')
    list_filter = ('character_class', 'race', 'role', 'server')
    search_fields = ('name', 'user__username')
