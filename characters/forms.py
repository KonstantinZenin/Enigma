from django import forms
from .models import GameCharacter

class CharacterForm(forms.ModelForm):
    class Meta:
        model = GameCharacter
        fields = ['name', 'race', 'character_class', 'role', 'server']
        labels = {
            'name': 'Имя персонажа',
            'race': 'Раса',
            'character_class': 'Класс',
            'role': 'Роль',
            'server': 'Сервер',
        }
        help_texts = {
            'name': 'Обязательное поле',
            'race': 'Обязательное поле',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'race': forms.TextInput(attrs={'class': 'form-control'}),
            'character_class': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'server': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        race = cleaned_data.get('race')
        
        if not name:
            self.add_error('name', 'Это поле обязательно для заполнения')
        if not race:
            self.add_error('race', 'Это поле обязательно для заполнения')
        
        return cleaned_data
