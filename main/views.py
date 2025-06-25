from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Teacher  # ← не забудь импортировать

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
                        user = User.objects.create_user(username=username, password=password, is_staff=True)
                        Teacher.objects.create(full_name=username, user=user)
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
                        Teacher.objects.filter(user=user).delete()
                        user.delete()
                        messages.success(request, f"Преподаватель '{user.username}' удалён.")
                    else:
                        messages.warning(request, "Нельзя удалить суперпользователя.")
                except User.DoesNotExist:
                    messages.error(request, "Пользователь не найден.")

            elif action == 'add_teacher':
                full_name = request.POST.get('full_name')
                teacher_type = request.POST.get('teacher_type')
                position = request.POST.get('position')
                rate = request.POST.get('rate')
                degree = request.POST.get('degree')
                rank = request.POST.get('rank')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                birthday = request.POST.get('birthday') or None
                address = request.POST.get('address')

                # Проверка обязательных полей
                if not full_name or not teacher_type or not position or not rate:
                    messages.error(request, "Поля ФИО, Тип, Должность и Ставка обязательны для заполнения.")
                else:
                    Teacher.objects.create(
                        full_name=full_name,
                        teacher_type=teacher_type,
                        position=position,
                        rate=rate,
                        degree=degree or None,
                        rank=rank or None,
                        email=email or None,
                        phone=phone or None,
                        birthday=birthday,
                        address=address or None
                    )
                    messages.success(request, f"Преподаватель '{full_name}' успешно добавлен.")
            elif action == 'delete_teacher':
                teacher_id = request.POST.get('delete_teacher')
                try:
                   teacher = Teacher.objects.get(id=teacher_id)
                   teacher.delete()
                   messages.success(request, f"Преподаватель '{teacher.full_name}' удалён.")
                except Teacher.DoesNotExist:
                    messages.error(request, "Преподаватель не найден.")
          

        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        teachers = Teacher.objects.all()
        return render(request, 'main/admin_dashboard.html', {
            'staff_users': staff_users,
            'teachers': teachers
        })

    elif request.user.is_staff:
        return render(request, 'main/teacher_dashboard.html')
    else:
        return render(request, 'main/student_dashboard.html')