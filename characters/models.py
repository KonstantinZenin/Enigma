from django.db import models
from users.models import GuildMember

class GameCharacter(models.Model):
    """
    Модель игрового персонажа пользователя
    """
    ROLE_CHOICES = [
        ('Tank', 'Танк'),
        ('Healer', 'Хилер'),
        ('DPS', 'ДД'),
    ]
    
    user = models.ForeignKey(GuildMember, on_delete=models.CASCADE, related_name='characters', verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Имя персонажа")
    character_class = models.CharField(max_length=50, verbose_name="Класс")
    race = models.CharField(max_length=50, verbose_name="Раса")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль")
    server = models.CharField(max_length=100, verbose_name="Сервер")

    def __str__(self):
        return f"{self.name} ({self.character_class})"
