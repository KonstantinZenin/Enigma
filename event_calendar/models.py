from django.db import models
from users.models import GuildMember
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True)
    start_time = models.DateTimeField(verbose_name=_('Время начала'))
    end_time = models.DateTimeField(verbose_name=_('Время окончания'))
    creator = models.ForeignKey(
        GuildMember,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name=_('Создатель')
    )
    participants = models.ManyToManyField(
        GuildMember,
        related_name='events',
        blank=True,
        verbose_name=_('Участники')
    )
    max_participants = models.PositiveIntegerField(
        verbose_name=_('Макс. участников'),
        null=True,
        blank=True
    )
    is_official = models.BooleanField(
        default=False,
        verbose_name=_('Официальное событие')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Событие')
        verbose_name_plural = _('События')
        ordering = ['start_time']

    def __str__(self):
        return self.title

    def clean(self):
        from django.utils import timezone
        
        # Проверка наличия значений времени
        if not self.start_time or not self.end_time:
            raise ValidationError(_('Необходимо указать время начала и окончания события'))
        
        # Проверка что событие не начинается в прошлом
        current_time = timezone.now()
        if timezone.is_naive(self.start_time):
            # Если время наивное, преобразуем в осведомленное
            self.start_time = timezone.make_aware(self.start_time)
        
        if self.start_time < current_time:
            raise ValidationError(_("Событие не может начинаться в прошлом"))
        
        # Проверка временных конфликтов
        if self.start_time >= self.end_time:
            raise ValidationError(_('Время окончания должно быть позже времени начала'))
        
        # Убедимся что end_time тоже осведомленное
        if timezone.is_naive(self.end_time):
            self.end_time = timezone.make_aware(self.end_time)
        
        # Проверка пересечений с другими событиями
        overlapping_events = Event.objects.filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        
        if overlapping_events.exists():
            raise ValidationError(_('Событие пересекается по времени с другим событием'))
