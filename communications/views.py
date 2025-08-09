from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_view(request):
    # Получаем последние 50 сообщений
    messages = Message.objects.order_by('-timestamp')[:50]
    return render(request, 'communications/chat.html', {'messages': messages})
