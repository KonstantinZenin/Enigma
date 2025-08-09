from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Event
from datetime import datetime

class EventForm(forms.ModelForm):
    start_time_date = forms.DateField(
        label=_('Дата начала'),
        widget=forms.DateInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    start_time_time = forms.TimeField(
        label=_('Время начала'),
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'max_participants', 'is_official']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk or 'start_time' in self.initial:
            # Если форма редактирования или есть начальное значение
            start_time = self.instance.start_time if self.instance.pk else self.initial.get('start_time')
            if start_time:
                self.fields['start_time_date'].initial = start_time.date()
                self.fields['start_time_time'].initial = start_time.time()
                self.fields['start_time'].widget = forms.HiddenInput()
        else:
            # Для нового события без предустановки
            self.fields['start_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    def clean(self):
        from django.utils import timezone
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_time_date')
        start_time = cleaned_data.get('start_time_time')
        
        if start_date and start_time:
            # Объединяем дату и время в datetime
            naive_datetime = datetime.combine(start_date, start_time)
            # Преобразуем в осведомленное время
            cleaned_data['start_time'] = timezone.make_aware(naive_datetime)
        
        return cleaned_data
