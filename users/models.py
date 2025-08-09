from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
import uuid

class GuildMember(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='default_avatar.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    telegram_username = models.CharField(max_length=32, blank=True, null=True)
    vk_id = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return str(self.username)

class InviteCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creator = models.ForeignKey(GuildMember, on_delete=models.CASCADE, related_name='created_invites')
    used_by = models.ForeignKey(GuildMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_invite')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.code)
