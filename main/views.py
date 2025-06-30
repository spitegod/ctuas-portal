
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Teacher, FirstSem, SecondSem
from django.db.models import Q


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # авторизуем независимо от прав
            return redirect('dashboard')  # там разруливаем, куда перекинуть
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

            # === Добавление пользователя ===
            if action == 'add':
                username = request.POST.get('username')
                password = request.POST.get('password')
                teacher_id = request.POST.get('teacher_id')

                if not username or not password:
                    messages.error(request, "Имя пользователя и пароль обязательны.")
                elif User.objects.filter(username=username).exists():
                    messages.warning(request, f"Пользователь '{username}' уже существует.")
                else:
                    user = User.objects.create_user(username=username, password=password, is_staff=True)

                    if teacher_id:
                        try:
                            teacher = Teacher.objects.get(id=teacher_id)
                            if teacher.user:
                                messages.warning(request, f"У преподавателя '{teacher.full_name}' уже есть логин.")
                            else:
                                teacher.user = user
                                teacher.save()
                                messages.success(request, f"Пользователь '{username}' привязан к преподавателю '{teacher.full_name}'.")
                        except Teacher.DoesNotExist:
                            messages.error(request, "Преподаватель не найден.")
                    else:
                        Teacher.objects.create(full_name=username, user=user)
                        messages.success(request, f"Создан новый преподаватель и пользователь '{username}'.")

            # === Удаление пользователя ===
            elif action == 'delete':
                user_id = request.POST.get('delete_user')
                try:
                    user = User.objects.get(id=user_id)
                    if user.is_superuser:
                        messages.warning(request, "Нельзя удалить суперпользователя.")
                    else:
                        Teacher.objects.filter(user=user).update(user=None)
                        user.delete()
                        messages.success(request, f"Пользователь '{user.username}' удалён.")
                except User.DoesNotExist:
                    messages.error(request, "Пользователь не найден.")

            # === Изменение прав доступа ===
            elif action == 'update_permissions':
                user_id = request.POST.get("user_id")
                is_staff = request.POST.get("is_staff") == "True"
                is_superuser = request.POST.get("is_superuser") == "True"

                try:
                    user = User.objects.get(id=user_id)
                    if user == request.user and not is_superuser:
                        messages.warning(request, "Нельзя снять права суперпользователя у самого себя.")
                    else:
                        user.is_staff = is_staff
                        user.is_superuser = is_superuser
                        user.save()
                        messages.success(request, f"Права пользователя '{user.username}' обновлены.", extra_tags="access")
                except User.DoesNotExist:
                    messages.error(request, "Пользователь не найден.", extra_tags="access")

            # === Добавление преподавателя ===
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

                if not full_name or not teacher_type or not position or not rate:
                    messages.error(request, "Поля ФИО, Тип, Должность и Ставка обязательны.")
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

            # === Удаление преподавателя ===
            elif action == 'delete_teacher':
                teacher_id = request.POST.get('delete_teacher')
                try:
                    teacher = Teacher.objects.get(id=teacher_id)
                    name = teacher.full_name
                    if teacher.user:
                        teacher.user = None
                        teacher.save()
                    teacher.delete()
                    messages.success(request, f"Преподаватель '{name}' удалён.")
                except Teacher.DoesNotExist:
                    messages.error(request, "Преподаватель не найден.")

        # === Подготовка данных для отображения ===
        staff_users = User.objects.filter(
            Q(is_staff=True) | Q(teacher__isnull=False)
        ).distinct()

        teachers = Teacher.objects.all()
        discipines_firstsem = FirstSem.objects.all()
        discipines_secondsem = SecondSem.objects.all()

        return render(request, 'main/admin_dashboard.html', {
            'staff_users': staff_users,
            'teachers': teachers,
            'disciplines_firstsem': discipines_firstsem,
            'discipines_secondsem': discipines_secondsem,
        })

    # === Для обычных преподавателей ===
    elif request.user.is_staff:
        return render(request, 'main/teacher_dashboard.html')

    # === Для студентов (если реализовано) ===
    else:
        return render(request, 'main/student_dashboard.html')