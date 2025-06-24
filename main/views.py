from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'main/login.html', {'error': 'Доступ разрешён только заведующему кафедры'})
        else:
            return render(request, 'main/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'main/login.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'add':
                username = request.POST.get('username')
                password = request.POST.get('password')

                if username and password:
                    if not User.objects.filter(username=username).exists():
                        # Всегда создаём как преподавателя
                        User.objects.create_user(username=username, password=password, is_staff=True)
                        messages.success(request, f"Преподаватель '{username}' успешно добавлен.")
                    else:
                        messages.warning(request, f"Пользователь '{username}' уже существует.")
                else:
                    messages.error(request, "Имя пользователя и пароль обязательны.")

            elif action == 'delete':
                user_id = request.POST.get('delete_user')
                try:
                    user = User.objects.get(id=user_id)
                    if not user.is_superuser:
                        user.delete()
                        messages.success(request, f"Преподаватель '{user.username}' удалён.")
                    else:
                        messages.warning(request, "Нельзя удалить суперпользователя.")
                except User.DoesNotExist:
                    messages.error(request, "Пользователь не найден.")

        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        return render(request, 'main/admin_dashboard.html', {'staff_users': staff_users})
    
    elif request.user.is_staff:
        return render(request, 'main/teacher_dashboard.html')
    else:
        return render(request, 'main/student_dashboard.html')