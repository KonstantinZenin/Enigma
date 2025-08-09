from django.db import models
from users.models import GuildMember

class GameCharacter(models.Model):
    """
    Модель игрового персонажа пользователя
    """
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('archived', 'В архиве'),
        ('banned', 'Запрещён в мире'),
    ]
    
    ROLE_CHOICES = [
        ('Tank', 'Танк'),
        ('Healer', 'Хилер'),
        ('DPS', 'ДД'),
    ]
    
    user = models.ForeignKey(GuildMember, on_delete=models.CASCADE, related_name='characters', verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Имя персонажа")
    character_class = models.CharField(max_length=50, verbose_name="Класс", blank=True, null=True)
    race = models.CharField(max_length=50, verbose_name="Раса")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль", blank=True, null=True)
    server = models.CharField(max_length=100, verbose_name="Сервер", blank=True, null=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Статус персонажа"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} ({self.character_class})"
