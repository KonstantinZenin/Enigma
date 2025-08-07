from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Event
from .forms import EventForm
from users.models import GuildMember
from .telegram_utils import send_telegram_reminder

class EventListView(ListView):
    model = Event
    template_name = 'event_calendar/event_list.html'
    context_object_name = 'events'
    ordering = ['-start_time']

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def get_initial(self):
        from django.utils import timezone
        initial = super().get_initial()
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                # Преобразуем строку даты в объект datetime (начало дня)
                naive_datetime = datetime.strptime(date_str, '%Y-%m-%d')
                # Преобразуем в осведомленное время
                initial['start_time'] = timezone.make_aware(naive_datetime)
            except (ValueError, TypeError):
                pass
        return initial
    template_name = 'event_calendar/event_form.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        messages.success(self.request, _('Событие успешно создано'))
        response = super().form_valid(form)
        # Отправляем напоминание создателю
        try:
            send_telegram_reminder(self.object, self.request.user)
        except Exception as e:
            # Логируем ошибку, но не прерываем выполнение
            print(f"Ошибка при отправке Telegram напоминания: {e}")
        return response
    
    def get_success_url(self):
        return reverse_lazy('event_calendar:event_detail', kwargs={'pk': self.object.pk})

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_calendar/event_form.html'
    
    def form_valid(self, form):
        try:
            form.instance.clean()
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        messages.success(self.request, _('Событие успешно обновлено'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('event_calendar:event_detail', kwargs={'pk': self.object.pk})

from django.http import JsonResponse
from django.core import serializers

class EventCalendarView(ListView):
    model = Event
    template_name = 'event_calendar/event_calendar.html'

from django.views import View
from django.urls import reverse

class EventJsonView(View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        print(f"Found {len(events)} events in database")
        data = []
        for event in events:
            # Логирование для отладки временных зон
            print(f"Event: {event.title}")
            print(f"  DB start: {event.start_time} | TZ: {event.start_time.tzinfo}")
            print(f"  Local start: {event.start_time.astimezone()}")
            
            data.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat() if event.end_time else None,
                'url': reverse('event_calendar:event_detail', kwargs={'pk': event.pk}),
                'maxParticipants': event.max_participants,
                'participantsCount': event.participants.count(),
                'isOfficial': event.is_official,
                'startLocal': event.start_time.astimezone().isoformat(),
                'endLocal': event.end_time.astimezone().isoformat() if event.end_time else None
            })
        print(f"Returning {len(data)} events in JSON response")
        return JsonResponse(data, safe=False)

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_calendar/event_detail.html'
    context_object_name = 'event'

from django.shortcuts import get_object_or_404, redirect
from django.views import View

class EventJoinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        # Проверяем лимит участников только если он установлен
        if event.max_participants is not None and event.participants.count() >= event.max_participants:
            messages.error(request, _('Достигнут лимит участников'))
        else:
            event.participants.add(request.user)
            messages.success(request, _('Вы успешно присоединились к событию'))
            # Отправляем напоминание участнику
            try:
                send_telegram_reminder(event, request.user)
            except Exception as e:
                # Логируем ошибку, но не прерываем выполнение
                print(f"Ошибка при отправке Telegram напоминания: {e}")
        return redirect('event_calendar:event_detail', pk=pk)

class EventLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.participants.remove(request.user)
        messages.success(request, _('Вы вышли из события'))
        return redirect('event_calendar:event_detail', pk=pk)
