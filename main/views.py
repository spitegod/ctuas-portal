
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Teacher, FirstSem, SecondSem
from django.db.models import Q
from django.shortcuts import render, redirect
from main.models import Teacher, EducationalMethodicalWork, OrganizationalMethodicalWork,ResearchWork
from .models import Teacher, EducationalMethodicalWork, OrganizationalMethodicalWork, ResearchWork, ContractResearchWork,ScientificMethodicalWork
from .forms import EducationalMethodicalWorkForm, OrganizationalMethodicalWorkForm, ResearchWorkForm, ContractResearchWorkForm


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
         return teacher_dashboard(request)

   

    # === Для студентов (если реализовано) ===
    else:
        return render(request, 'main/student_dashboard.html')
    
def teacher_dashboard(request):
    teacher = request.user.teacher

    # === Добавление учебно-методической работы ===
    if request.method == 'POST' and request.POST.get("form_type") == "teaching_method":
        EducationalMethodicalWork.objects.create(
            teacher=teacher,
            title=request.POST.get("title"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            completed=request.POST.get("completed")
        )
        messages.success(request, "Учебно-методическая работа добавлена.")
        return redirect('/dashboard?tab=2')

    # === Удаление учебно-методической работы ===
    if request.method == 'POST' and request.POST.get("delete_teaching_method"):
        EducationalMethodicalWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
        messages.success(request, "Запись удалена.")
        return redirect('/dashboard?tab=2')

    # === Добавление орг.-методической работы ===
    if request.method == 'POST' and request.POST.get("form_type") == "organizational_method":
        OrganizationalMethodicalWork.objects.create(
            teacher=teacher,
            title=request.POST.get("title"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            completed=request.POST.get("completed")
        )
        messages.success(request, "Орг.-методическая работа добавлена.")
        return redirect('/dashboard?tab=3')

    # === Удаление орг.-методической работы ===
    if request.method == 'POST' and request.POST.get("delete_organizational_method"):
        OrganizationalMethodicalWork.objects.filter(id=request.POST.get("delete_organizational_method"), teacher=teacher).delete()
        messages.success(request, "Запись удалена.")
        return redirect('/dashboard?tab=3')

    # === Добавление научно-исследовательской работы ===
    if request.method == 'POST' and request.POST.get("form_type") == "research_work":
        ResearchWork.objects.create(
            teacher=teacher,
            topic=request.POST.get("topic"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            completed=request.POST.get("completed")
        )
        messages.success(request, "Научно-исследовательская работа добавлена.")
        return redirect('/dashboard?tab=4')

    # === Удаление научно-исследовательской работы ===
    if request.method == 'POST' and request.POST.get("delete_research_work"):
        ResearchWork.objects.filter(id=request.POST.get("delete_research_work"), teacher=teacher).delete()
        messages.success(request, "Запись удалена.")
        return redirect('/dashboard?tab=4')

    # === Добавление хоздоговорной НИР ===
    if request.method == 'POST' and request.POST.get("form_type") == "contract_research":
        ContractResearchWork.objects.create(
            teacher=teacher,
            topic=request.POST.get("topic"),
            position=request.POST.get("position"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            completed=request.POST.get("completed")
        )
        messages.success(request, "Запись по хоздоговорной НИР добавлена.")
        return redirect('/dashboard?tab=5')

    # === Удаление хоздоговорной НИР ===
    if request.method == 'POST' and request.POST.get("delete_contract_research"):
        ContractResearchWork.objects.filter(id=request.POST.get("delete_contract_research"), teacher=teacher).delete()
        messages.success(request, "Запись удалена.")
        return redirect('/dashboard?tab=5')

    # === Добавление научно-методической работы ===
    if request.method == 'POST' and request.POST.get("form_type") == "scientific_method":
        ScientificMethodicalWork.objects.create(
            teacher=teacher,
            topic=request.POST.get("topic"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date") or None,
            completed=request.POST.get("completed")
        )
        messages.success(request, "Научно-методическая работа добавлена.")
        return redirect('/dashboard?tab=6')

    # === Удаление научно-методической работы ===
    if request.method == 'POST' and request.POST.get("delete_scientific_method"):
        ScientificMethodicalWork.objects.filter(id=request.POST.get("delete_scientific_method"), teacher=teacher).delete()
        messages.success(request, "Запись удалена.")
        return redirect('/dashboard?tab=6')

    # === Выборки всех типов работ ===
    edu_works = EducationalMethodicalWork.objects.filter(teacher=teacher)
    org_works = OrganizationalMethodicalWork.objects.filter(teacher=teacher)
    research_works = ResearchWork.objects.filter(teacher=teacher)
    contract_works = ContractResearchWork.objects.filter(teacher=teacher)
    scientific_works = ScientificMethodicalWork.objects.filter(teacher=teacher)

    return render(request, 'main/teacher_dashboard.html', {
        'works': edu_works,
        'org_works': org_works,
        'research_works': research_works,
        'contract_works': contract_works,
        'scientific_works': scientific_works,
    })