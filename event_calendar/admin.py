from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'creator', 'max_participants', 'is_official')
    list_filter = ('is_official', 'start_time')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'
    filter_horizontal = ('participants',)
    
    # Добавляем переводы для заголовков
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].label = _('Название')
        form.base_fields['description'].label = _('Описание')
        form.base_fields['start_time'].label = _('Время начала')
        form.base_fields['end_time'].label = _('Время окончания')
        form.base_fields['max_participants'].label = _('Макс. участников')
        form.base_fields['is_official'].label = _('Официальное')
        return form
