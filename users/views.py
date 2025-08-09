from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import RegistrationForm, ProfileEditForm, LoginForm
from .models import InviteCode
from characters.models import GameCharacter

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                return redirect("users:profile")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def profile_view(request):
    # Получаем персонажей текущего пользователя
    # Игнорировать предупреждение Pylint - GameCharacter имеет менеджер objects
    # pylint: disable=no-member
    character_list = GameCharacter.objects.filter(user=request.user).order_by("-created_at")
    
    # Пагинация
    paginator = Paginator(character_list, 10)
    page_number = request.GET.get("page")
    characters = paginator.get_page(page_number)
    
    return render(request, "users/profile.html", {"user": request.user, "characters": characters})

@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("users:profile")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return redirect("landing")

@login_required
def generate_invite_view(request):
    new_code = InviteCode(creator=request.user)
    new_code.save()
    messages.success(request, f"Новый инвайт-код создан: {new_code.code}")
    return redirect("users:profile")

def invite_code_form_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        # Игнорировать предупреждение Pylint
        # pylint: disable=no-member
        if InviteCode.objects.filter(code=code, is_active=True).exists():
            return redirect(f'{reverse("users:register")}?code={code}')
        messages.error(request, "Неверный или неактивный инвайт-код")
    return render(request, "users/invite_form.html")

def invite_error_view(request):
    return render(request, "users/invite_error.html")

def register_view(request):
    invite_code = request.GET.get("code")
    # Игнорировать предупреждение Pylint
    # pylint: disable=no-member
    if not invite_code or not InviteCode.objects.filter(code=invite_code, is_active=True).exists():
        return redirect("users:invite_error")
    
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            try:
                # Игнорировать предупреждение Pylint
                # pylint: disable=no-member
                code_obj = InviteCode.objects.get(code=invite_code)
                code_obj.used_by = user
                code_obj.is_active = False
                code_obj.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect("users:profile")
            except InviteCode.DoesNotExist:
                messages.error(request, "Инвайт-код не найден")
                return redirect("users:invite_error")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})
