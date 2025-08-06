from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    """
    Модель роли пользователя в гильдии
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")
    is_officer = models.BooleanField(default=False, verbose_name="Офицер")
    is_leader = models.BooleanField(default=False, verbose_name="Глава гильдии")

    def __str__(self):
        return str(self.name)


class GuildMember(AbstractUser):
    """
    Расширенная модель пользователя для хранения информации о членах гильдии.
    """
    # имя пользователя
    name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    # фамилия пользователя
    surname = models.CharField(max_length=150, verbose_name="Фамилия пользователя")
    # отчество пользователя
    patronymic = models.CharField(max_length=150, verbose_name="Отчество пользователя", blank=True, null=True)
    # дата рождения
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    # номер телефона
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)
    # адрес электронной почты
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    # аватар пользователя
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name="Аватар", blank=True, null=True)
    # телеграм-никнейм
    telegram_username = models.CharField(max_length=150, verbose_name="Телеграм-никнейм", unique=True)
    # vk-id 
    vk_id = models.CharField(max_length=150, verbose_name="VK ID", unique=True, blank=True, null=True)
    # адрес
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)
    # дата регистрации
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    # роль в гильдии
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль в гильдии")

    # Переопределение полей для разрешения конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="guild_member_groups",
        related_query_name="guild_member",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="guild_member_permissions",
        related_query_name="guild_member",
    )

    def get_avatar(self):
        from django.conf import settings
        return self.avatar if self.avatar else settings.DEFAULT_AVATAR_URL

    @property
    def avatar_url(self):
        from django.conf import settings
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return settings.DEFAULT_AVATAR_URL
