from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import GameCharacter
from .forms import CharacterForm
from users.models import GuildMember

class CharacterCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания нового игрового персонажа"""
    
    model = GameCharacter
    form_class = CharacterForm
    template_name = 'characters/character_form.html'
    
    def form_valid(self, form):
        """
        Добавляет текущего пользователя как владельца персонажа.
        
        Автоматически связывает создаваемого персонажа с объектом GuildMember,
        соответствующим текущему пользователю.
        """
        guild_member, created = GuildMember.objects.get_or_create(user=self.request.user)
        form.instance.user = guild_member
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})

class CharacterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GameCharacter
    form_class = CharacterForm
    template_name = 'characters/character_form.html'
    
    def test_func(self):
        """
        Проверяет права доступа: только владелец персонажа может его редактировать.
        
        Returns:
            bool: True если текущий пользователь - владелец персонажа, иначе False
        """
        character = self.get_object()
        return character.user.user_id == self.request.user.id
    
    def get_success_url(self):
        character = self.get_object()
        return reverse_lazy('characters:detail', kwargs={'pk': character.pk})

class CharacterDetailView(DetailView):
    model = GameCharacter
    template_name = 'characters/character_detail.html'
    context_object_name = 'character'

class CharacterListView(ListView):
    model = GameCharacter
    template_name = 'characters/character_list.html'
    context_object_name = 'characters'
    paginate_by = 10
    
    def get_queryset(self):
        return GameCharacter.objects.filter(status='active').order_by('-created_at')

class UserCharacterListView(ListView):
    model = GameCharacter
    template_name = 'characters/user_character_list.html'
    context_object_name = 'characters'
    paginate_by = 10
    
    def get_queryset(self):
        return GameCharacter.objects.filter(
            user__pk=self.kwargs['pk'], 
            status='active'
        ).order_by('-created_at')
