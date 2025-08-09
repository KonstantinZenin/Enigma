from django.db import models
from django.conf import settings
from users.models import GuildMember  # Импорт модели пользователя

class Message(models.Model):
    """Модель для хранения сообщений чата"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Пользователь'
    )
    content = models.TextField(verbose_name='Содержание')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    room = models.CharField(
        max_length=100,
        default='main',
        verbose_name='Комната'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-timestamp']

    def __str__(self) -> str:
        # Безопасное получение имени пользователя и превью сообщения
        username = self.user.username if hasattr(self.user, 'username') else "Unknown"
        content_preview = str(self.content)[:20] if self.content else ""
        return f'{username}: {content_preview}'
