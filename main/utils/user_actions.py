from django.contrib.auth.models import User
from main.models import Teacher
from django.contrib import messages
from main.models import Teacher, TeacherPermission
from django.shortcuts import redirect


def handle_add_user(request):
    """Добавление пользователя преподавателем или администратором"""

    # Проверка прав доступа
    if not request.user.is_superuser:
        teacher = Teacher.objects.filter(user=request.user).first()
        if not teacher:
            messages.error(request, "Вы не привязаны к преподавателю.")
            return

        permission = TeacherPermission.objects.filter(teacher=teacher).first()
        if not permission or not permission.can_manage_accounts:
            messages.error(request, "У вас нет прав для добавления пользователей.")
            return

    # Получение данных формы
    username = request.POST.get("username")
    password = request.POST.get("password")
    teacher_id = request.POST.get("teacher_id")

    # Валидация
    if not username or not password:
        messages.error(request, "Имя пользователя и пароль обязательны.")
        return

    if User.objects.filter(username=username).exists():
        messages.error(request, "Пользователь с таким именем уже существует.")
        return

    # Создание пользователя
    new_user = User.objects.create_user(username=username, password=password, is_staff=True)

    # Привязка к преподавателю
    if teacher_id:
        t = Teacher.objects.filter(id=teacher_id, user=None).first()
        if t:
            t.user = new_user
            t.save()
    else:
       
        Teacher.objects.create(
            full_name=f"Преподаватель {username}",
            teacher_type='Внутр',  # Можно заменить на значение по умолчанию
            position="—",
            rate="1.0",
            user=new_user
        )

    messages.success(request, f"Пользователь '{username}' успешно добавлен.")



def handle_delete_user(request, user_or_teacher=None):
    if isinstance(user_or_teacher, Teacher):
        user = user_or_teacher.user
    else:
        user_id = request.POST.get("user_id")
        user = User.objects.filter(id=user_id).first()

    if not user:
        messages.error(request, "Пользователь не найден.")
        return

    if user != request.user and user.is_superuser:
        messages.error(request, "Нельзя удалить другого суперпользователя.")
        return


    if user == request.user:
        messages.warning(request, "Нельзя удалить самого себя.")
        return

    teacher = Teacher.objects.filter(user=user).first()
    if teacher:
        teacher.user = None
        teacher.save()

    user.delete()
    messages.success(request, "Пользователь успешно удалён.")
    
def handle_update_permissions(request, user_id):
    is_staff = request.POST.get("is_staff") == "True"
    is_superuser = request.POST.get("is_superuser") == "True"
    can_manage_accounts = request.POST.get("can_manage_accounts") == "True"
    can_edit_ip = request.POST.get("can_edit_ip") == "True"
    can_edit_pps = request.POST.get("can_edit_pps") == "True"

    try:
        user = User.objects.get(id=user_id)

        
        if user != request.user and user.is_superuser:
            messages.error(request, "Нельзя редактировать другого суперпользователя.")
            return

        
        if user == request.user and not is_superuser:
            messages.warning(request, "Нельзя снять права суперпользователя у самого себя.")
            return

        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        teacher = Teacher.objects.filter(user=user).first()
        if teacher:
            perm, _ = TeacherPermission.objects.get_or_create(teacher=teacher)
            perm.can_manage_accounts = can_manage_accounts
            perm.can_edit_ip = can_edit_ip
            perm.can_edit_pps = can_edit_pps
            perm.save()
        else:
            messages.warning(request, f"У пользователя '{user.username}' не найден преподаватель. Права не обновлены.")

        messages.success(request, f"Права пользователя '{user.username}' успешно обновлены.", extra_tags="access")

    except User.DoesNotExist:
        messages.error(request, "Пользователь не найден.", extra_tags="access")
