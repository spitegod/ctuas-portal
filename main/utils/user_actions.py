from django.contrib.auth.models import User
from main.models import Teacher
from django.contrib import messages
from main.models import Teacher, TeacherPermission
from django.shortcuts import redirect


def handle_add_user(request):
    """Добавление пользователя преподавателем или администратором"""
    # Администратор всегда имеет доступ
    if not request.user.is_superuser:
        # Проверка наличия разрешения у преподавателя
        teacher = Teacher.objects.filter(user=request.user).first()
        if not teacher:
            messages.error(request, "Вы не привязаны к преподавателю.")
            return

        permission = TeacherPermission.objects.filter(teacher=teacher).first()
        if not permission or not permission.can_manage_accounts:
            messages.error(request, "У вас нет прав для добавления пользователей.")
            return

    username = request.POST.get("username")
    password = request.POST.get("password")
    teacher_id = request.POST.get("teacher_id")

    if not username or not password:
        messages.error(request, "Имя пользователя и пароль обязательны.")
        return

    if User.objects.filter(username=username).exists():
        messages.error(request, "Пользователь с таким именем уже существует.")
        return

    new_user = User.objects.create_user(username=username, password=password, is_staff=True)

    if teacher_id:
        t = Teacher.objects.filter(id=teacher_id, user=None).first()
        if t:
            t.user = new_user
            t.save()

    messages.success(request, f"Пользователь '{username}' добавлен.")
    


def handle_delete_user(request, teacher=None):
    user_id = request.POST.get("delete_user")
    print(f"[DEBUG] Удаляем пользователя: {user_id}")

    try:
        user_to_delete = User.objects.get(id=user_id)

        # Защита от самоуничтожения
        if request.user == user_to_delete:
            messages.error(request, "Вы не можете удалить самого себя.")
            return False

        # Преподаватель не может удалить админа
        if user_to_delete.is_superuser:
            messages.error(request, "Нельзя удалить администратора.")
            return False

        # Если удаляет не суперпользователь, проверяем права
        if teacher:
            permissions, _ = TeacherPermission.objects.get_or_create(teacher=teacher)

            if not permissions.can_manage_accounts:
                messages.error(request, "У вас нет прав на удаление пользователей.")
                return False

        # Всё прошло — удаляем
        user_to_delete.delete()
        messages.success(request, "Пользователь успешно удалён.")
        return True

    except User.DoesNotExist:
        messages.error(request, "Пользователь не найден.")
        return False