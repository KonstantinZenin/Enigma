from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import GuildMember

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'users/custom_clearable_file_input.html'

class RegistrationForm(UserCreationForm):
    telegram_username = forms.CharField(
        max_length=32,
        required=True,
        help_text='Обязательное поле. Введите ваш Telegram username'
    )
    
    class Meta:
        model = GuildMember
        fields = ('username', 'telegram_username', 'password1', 'password2')

class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Используем кастомный виджет для поля аватара
        self.fields['avatar'].widget = CustomClearableFileInput()
    
    class Meta:
        model = GuildMember
        fields = (
            'avatar', 'name', 'surname', 'patronymic', 
            'birth_date', 'phone_number', 'telegram_username', 
            'vk_id', 'address'
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(AuthenticationForm):
    pass
