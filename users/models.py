from os import name
from django.db import models
from django.contrib.auth.models import AbstractUser


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
    avatar = models.ImageField(upload_to='avatars/', verbose_name="Аватар", blank=True, null=True)
    # телеграм-никнейм
    telegram_username = models.CharField(max_length=150, verbose_name="Телеграм-никнейм", unique=True)
    # vk-id 
    vk_id = models.CharField(max_length=150, verbose_name="VK ID", unique=True, blank=True, null=True)
    # адрес
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)
    # дата регистрации
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")