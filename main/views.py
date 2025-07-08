
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Teacher, FirstSem, SecondSem, MethodicalWork, OrgMethodicalWork, SciResearchWork, ContractWork, SciMethodicalWork, PublicWork, Remark
from django.db.models import Q
from django.shortcuts import render, redirect
from main.models import Teacher, EducationalMethodicalWork, OrganizationalMethodicalWork,ResearchWork
from .models import Teacher, EducationalMethodicalWork, OrganizationalMethodicalWork, ResearchWork, ContractResearchWork,ScientificMethodicalWork,SocialEducationalWork,TeacherRemark, QualificationUpgrade, QualificationUpgrade, PublishedSciWork, Raising, Recommendation,TeacherPermission
from .forms import EducationalMethodicalWorkForm, OrganizationalMethodicalWorkForm, ResearchWorkForm, ContractResearchWorkForm
import openpyxl
from django.http import HttpResponse
from io import BytesIO
import openpyxl
from openpyxl.utils import get_column_letter
from datetime import datetime


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

                can_edit_publications = request.POST.get("can_edit_publications") == "True"
                can_edit_ip = request.POST.get("can_edit_ip") == "True"
                can_edit_pps = request.POST.get("can_edit_pps") == "True"
                can_edit_org_work = request.POST.get("can_edit_org_work") == "True"
                can_edit_sci_work = request.POST.get("can_edit_sci_work") == "True"
                
                try:
                    user = User.objects.get(id=user_id)

                    if user == request.user and not is_superuser:
                        messages.warning(request, "Нельзя снять права суперпользователя у самого себя.")
                    else:      
                      user.is_staff = is_staff
                      user.is_superuser = is_superuser
                      user.save()

                      teacher = Teacher.objects.filter(user=user).first()
                      if teacher:
                            permissions, _ = TeacherPermission.objects.get_or_create(teacher=teacher)
                            permissions.can_edit_publications = can_edit_publications
                            permissions.can_edit_ip = can_edit_ip
                            permissions.can_edit_pps = can_edit_pps
                            permissions.can_edit_org_work = can_edit_org_work
                            permissions.can_edit_sci_work = can_edit_sci_work
                            permissions.save()
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
            
            # === Выбор преподавателя ===
            elif action == 'select_ip_teacher':
                selected_teacher_id = request.POST.get('selected_teacher_id')
                if selected_teacher_id:
                    request.session['selected_teacher_id'] = selected_teacher_id

        # === Подготовка данных для отображения ===
        staff_users = User.objects.filter(
            Q(is_staff=True) | Q(teacher__isnull=False)
        ).distinct()

        selected_teacher = None
        selected_teacher_id = request.session.get('selected_teacher_id')

        if selected_teacher_id:
            try:
                selected_teacher = Teacher.objects.get(id=selected_teacher_id)
            except Teacher.DoesNotExist:
                selected_teacher = None
                request.session.pop('selected_teacher_id', None)

        teachers = Teacher.objects.all()
        discipines_firstsem = FirstSem.objects.filter(teacher=selected_teacher) if selected_teacher else []
        discipines_secondsem = SecondSem.objects.filter(teacher=selected_teacher) if selected_teacher else []
        edu_methodwork = EducationalMethodicalWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        org_methodwork = OrganizationalMethodicalWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        sci_researchwork = ResearchWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        contractwork = ContractResearchWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        sci_methodwork = ScientificMethodicalWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        published_sciwork = PublishedSciWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        social_eduwork = SocialEducationalWork.objects.filter(teacher=selected_teacher) if selected_teacher else []
        remark = TeacherRemark.objects.filter(teacher=selected_teacher) if selected_teacher else []
        raising = Raising.objects.filter(teacher=selected_teacher) if selected_teacher else []
        recommendation = Recommendation.objects.filter(teacher=selected_teacher) if selected_teacher else []

        return render(request, 'main/admin_dashboard.html', {
            'staff_users': staff_users,
            'teachers': teachers,
            'disciplines_firstsem': discipines_firstsem,
            'discipines_secondsem': discipines_secondsem,
            'edu_methodwork': edu_methodwork,
            'org_methodwork': org_methodwork,
            'sci_researchwork': sci_researchwork,
            'contractwork': contractwork,
            'sci_methodwork': sci_methodwork,
            'published_sciwork': published_sciwork,
            'social_eduwork': social_eduwork,
            'remark': remark,
            'raising': raising,
            'recommendation': recommendation,
            'selected_teacher': selected_teacher
        })

    # === Для обычных преподавателей ===
    elif request.user.is_staff:
         return teacher_dashboard(request)

   

    # === Для студентов (если реализовано) ===
    else:
        return render(request, 'main/student_dashboard.html')
    
def teacher_dashboard(request):
    teacher = request.user.teacher
    permissions = getattr(teacher, 'permissions', None)
    print(f"[DEBUG] can_edit_pps = {permissions.can_edit_pps if permissions else 'NO PERMS'}")
    last_initial = teacher.full_name.strip()[0].upper() if teacher.full_name else ''
    # === Выбор учебного года ===
    selected_year = request.GET.get("year") or request.session.get("selected_year")
    if not selected_year:
        current = datetime.now().year
        selected_year = f"{current-1}–{current}"
    request.session["selected_year"] = selected_year

    edit_id_tab2 = edit_id_tab3 = edit_id_tab4 = edit_id_tab5 = edit_id_tab6 = edit_id_tab8 = edit_id_tab9 = edit_id_tab10 = None
    edit_work_tab2 = edit_work_tab3 = edit_work_tab4 = edit_work_tab5 = edit_work_tab6 = edit_work_tab8 = edit_work_tab9 = edit_work_tab10 = None
    active_tab = int(request.GET.get("tab") or request.POST.get("active_tab") or 1)

    if request.method == 'POST':
        form_type = request.POST.get("form_type")

        # === Вкладка 2: Учебно-методическая ===
        if request.POST.get("edit_teaching_method"):
            edit_id_tab2 = request.POST.get("edit_teaching_method")
            edit_work_tab2 = EducationalMethodicalWork.objects.filter(id=edit_id_tab2, teacher=teacher).first()
            active_tab = 2

        elif form_type == "teaching_method":
            work_id = request.POST.get("work_id")
            academic_year = request.POST.get("academic_year", selected_year)
            if work_id:
                work = EducationalMethodicalWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.title = request.POST.get("title")
                    work.start_date = request.POST.get("start_date")
                    work.end_date = request.POST.get("end_date") or None
                    work.completed = request.POST.get("completed")
                    work.academic_year = academic_year
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                EducationalMethodicalWork.objects.create(
                    teacher=teacher,
                    title=request.POST.get("title"),
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date") or None,
                    completed=request.POST.get("completed"),
                    academic_year=academic_year 
                )
                messages.success(request, "Учебно-методическая работа добавлена.")
            return redirect(f'/dashboard?tab=2')

        elif form_type == "delete_teaching_method":
            EducationalMethodicalWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=2')

        # === Вкладка 3: Организационно-методическая ===
        if request.POST.get("edit_organizational_method"):
            edit_id_tab3 = request.POST.get("edit_organizational_method")
            edit_work_tab3 = OrganizationalMethodicalWork.objects.filter(id=edit_id_tab3, teacher=teacher).first()
            active_tab = 3

        elif form_type == "organizational_method":
            work_id = request.POST.get("work_id")
            if work_id:
                work = OrganizationalMethodicalWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.title = request.POST.get("title")
                    work.start_date = request.POST.get("start_date")
                    work.end_date = request.POST.get("end_date") or None
                    work.completed = request.POST.get("completed")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                OrganizationalMethodicalWork.objects.create(
                    teacher=teacher,
                    title=request.POST.get("title"),
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date") or None,
                    completed=request.POST.get("completed")
                )
                messages.success(request, "Орг.-методическая работа добавлена.")
            return redirect(f'/dashboard?tab=3')

        elif form_type == "delete_organizational_method":
            OrganizationalMethodicalWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=3')

        # === Вкладка 4: Научно-исследовательская ===
        if request.POST.get("edit_research_work"):
            edit_id_tab4 = request.POST.get("edit_research_work")
            edit_work_tab4 = ResearchWork.objects.filter(id=edit_id_tab4, teacher=teacher).first()
            active_tab = 4

        elif form_type == "research_work":
            work_id = request.POST.get("work_id")
            if work_id:
                work = ResearchWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.topic = request.POST.get("topic")
                    work.start_date = request.POST.get("start_date")
                    work.end_date = request.POST.get("end_date") or None
                    work.completed = request.POST.get("completed")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                ResearchWork.objects.create(
                    teacher=teacher,
                    topic=request.POST.get("topic"),
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date") or None,
                    completed=request.POST.get("completed")
                )
                messages.success(request, "Научно-исследовательская работа добавлена.")
            return redirect(f'/dashboard?tab=4')

        elif form_type == "delete_research_work":
            ResearchWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=4')

        # === Вкладка 5: Хоздоговорная НИР ===
        if request.POST.get("edit_contract_research"):
            edit_id_tab5 = request.POST.get("edit_contract_research")
            edit_work_tab5 = ContractResearchWork.objects.filter(id=edit_id_tab5, teacher=teacher).first()
            active_tab = 5

        elif form_type == "contract_research":
            work_id = request.POST.get("work_id")
            if work_id:
                work = ContractResearchWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.topic = request.POST.get("topic")
                    work.position = request.POST.get("position")
                    work.start_date = request.POST.get("start_date")
                    work.end_date = request.POST.get("end_date") or None
                    work.completed = request.POST.get("completed")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                ContractResearchWork.objects.create(
                    teacher=teacher,
                    topic=request.POST.get("topic"),
                    position=request.POST.get("position"),
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date") or None,
                    completed=request.POST.get("completed")
                )
                messages.success(request, "Хоздоговорная НИР добавлена.")
            return redirect(f'/dashboard?tab=5')

        elif form_type == "delete_contract_research":
            ContractResearchWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=5')

        # === Вкладка 6: Научно-методическая ===
        if request.POST.get("edit_scientific_method"):
            edit_id_tab6 = request.POST.get("edit_scientific_method")
            edit_work_tab6 = ScientificMethodicalWork.objects.filter(id=edit_id_tab6, teacher=teacher).first()
            active_tab = 6

        elif form_type == "scientific_method":
            work_id = request.POST.get("work_id")
            topic = request.POST.get("topic")

            if not topic:
                messages.error(request, "Поле 'Наименование темы' обязательно для заполнения.")
                return redirect(f'/dashboard?tab=6')

            if work_id:
                work = ScientificMethodicalWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.topic = topic
                    work.start_date = request.POST.get("start_date")
                    work.end_date = request.POST.get("end_date") or None
                    work.completed = request.POST.get("completed")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                ScientificMethodicalWork.objects.create(
                    teacher=teacher,
                    topic=topic,
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date") or None,
                    completed=request.POST.get("completed")
                )
                messages.success(request, "Научно-методическая работа добавлена.")
            return redirect(f'/dashboard?tab=6')

        elif form_type == "delete_scientific_method":
            ScientificMethodicalWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=6')

        # === Вкладка 8: Общественная работа ===
        if request.POST.get("edit_social_work"):
            edit_id_tab8 = request.POST.get("edit_social_work")
            edit_work_tab8 = SocialEducationalWork.objects.filter(id=edit_id_tab8, teacher=teacher).first()
            active_tab = 8

        elif form_type == "social_work":
            work_id = request.POST.get("work_id")
            if work_id:
                work = SocialEducationalWork.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.title = request.POST.get("title")
                    work.completed = request.POST.get("completed")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                SocialEducationalWork.objects.create(
                    teacher=teacher,
                    title=request.POST.get("title"),
                    completed=request.POST.get("completed")
                )
                messages.success(request, "Запись добавлена.")
            return redirect(f'/dashboard?tab=8')

        elif form_type == "delete_social_work":
            SocialEducationalWork.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=8')

        # === Вкладка 9: Замечания ===
        if request.POST.get("edit_remark"):
            edit_id_tab9 = request.POST.get("edit_remark")
            edit_work_tab9 = TeacherRemark.objects.filter(id=edit_id_tab9, teacher=teacher).first()
            active_tab = 9

        elif form_type == "teacher_remark":
            work_id = request.POST.get("work_id")
            if work_id:
                work = TeacherRemark.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.date = request.POST.get("date")
                    work.content = request.POST.get("content")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                TeacherRemark.objects.create(
                    teacher=teacher,
                    date=request.POST.get("date"),
                    content=request.POST.get("content")
                )
                messages.success(request, "Замечание добавлено.")
            return redirect(f'/dashboard?tab=9')

        elif form_type == "delete_teacher_remark":
            TeacherRemark.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=9')

        # === Вкладка 10: Повышение квалификации ===
        if request.POST.get("edit_qualification"):
            edit_id_tab10 = request.POST.get("edit_qualification")
            edit_work_tab10 = QualificationUpgrade.objects.filter(id=edit_id_tab10, teacher=teacher).first()
            active_tab = 10

        elif form_type == "qualification_upgrade":
            work_id = request.POST.get("work_id")
            date = request.POST.get("date")
            if not date:
                messages.error(request, "Поле 'Дата' обязательно для заполнения.")
                return redirect(f'/dashboard?tab=10')
    
            if work_id:
                work = QualificationUpgrade.objects.filter(id=work_id, teacher=teacher).first()
                if work:
                    work.title = request.POST.get("title")
                    work.location = request.POST.get("place")
                    work.document_number = request.POST.get("document_number")
                    work.date = request.POST.get("date")
                    work.duration = request.POST.get("duration")
                    work.volume = request.POST.get("volume")
                    work.save()
                    messages.success(request, "Запись обновлена.")
            else:
                QualificationUpgrade.objects.create(
                    teacher=teacher,
                    title=request.POST.get("title"),
                    location=request.POST.get("place"),
                    document_number=request.POST.get("document_number"),
                    date=request.POST.get("date")  or None,
                    duration=request.POST.get("duration"),
                    volume=request.POST.get("volume")
                )
                messages.success(request, "Повышение квалификации добавлено.")
            return redirect(f'/dashboard?tab=10')

        elif form_type == "delete_qualification_upgrade":
            QualificationUpgrade.objects.filter(id=request.POST.get("work_id"), teacher=teacher).delete()
            messages.success(request, "Запись удалена.")
            return redirect(f'/dashboard?tab=10')

    
    context = {
    # Данные по вкладкам
    'works': EducationalMethodicalWork.objects.filter(teacher=teacher, academic_year=selected_year),
    'org_works': OrganizationalMethodicalWork.objects.filter(teacher=teacher),
    'research_works': ResearchWork.objects.filter(teacher=teacher),
    'contract_works': ContractResearchWork.objects.filter(teacher=teacher),
    'scientific_works': ScientificMethodicalWork.objects.filter(teacher=teacher),
    'social_works': SocialEducationalWork.objects.filter(teacher=teacher),
    'teacher_remarks': TeacherRemark.objects.filter(teacher=teacher),
    'qualification_upgrades': QualificationUpgrade.objects.filter(teacher=teacher),
    
    'permissions': permissions,

    # Редактируемые записи
    'edit_work_tab2': edit_work_tab2,
    'edit_work_tab3': edit_work_tab3,
    'edit_work_tab4': edit_work_tab4,
    'edit_work_tab5': edit_work_tab5,
    'edit_work_tab6': edit_work_tab6,
    'edit_work_tab8': edit_work_tab8,
    'edit_work_tab9': edit_work_tab9,
    'edit_work_tab10': edit_work_tab10,

    # Учебные года
    'selected_year': selected_year,
    'available_years': ["2022–2023", "2023–2024", "2024–2025"],

    # Права доступа
    'can_edit_pps': permissions.can_edit_pps if permissions else False,

    # Преподаватели (для tab11, только если разрешено)
    'teachers': Teacher.objects.all() if permissions and permissions.can_edit_pps else [],

    # Остальное
    'active_tab': active_tab,
    'last_initial': last_initial,
}

    return render(request, 'main/teacher_dashboard.html', context)

def export_qualification_excel(request):
    teacher = request.user.teacher
    qualifications = QualificationUpgrade.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Повышение квалификации"

    headers = ["Название", "Место", "Номер документа", "Дата", "Срок", "Объём"]
    ws.append(headers)

    for q in qualifications:
        ws.append([
            q.title,
            q.location,
            q.document_number,
            q.date.strftime('%Y-%m-%d') if q.date else '',
            q.duration,
            q.volume
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="qualification.xlsx"'
    wb.save(response)
    return response

def export_teaching_excel(request):
    teacher = request.user.teacher
    selected_year = request.GET.get("year") or request.session.get("selected_year")

    if selected_year:
        works = EducationalMethodicalWork.objects.filter(teacher=teacher, academic_year=selected_year)
    else:
        works = EducationalMethodicalWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Учебно-методическая"

    ws.append(["Наименование", "Дата начала", "Дата окончания", "Отметка", "Учебный год"])
    for w in works:
        ws.append([w.title, w.start_date, w.end_date, w.completed, w.academic_year])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="teaching_{selected_year or "all"}.xlsx"'
    wb.save(response)
    return response

@login_required
def export_organizational_excel(request):
    teacher = request.user.teacher
    works = OrganizationalMethodicalWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Орг-методическая"

    ws.append(["Наименование", "Дата начала", "Дата окончания", "Отметка"])
    for w in works:
        ws.append([w.title, w.start_date, w.end_date, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="organizational.xlsx"'
    wb.save(response)
    return response


@login_required
def export_organizational_excel(request):
    teacher = request.user.teacher
    works = OrganizationalMethodicalWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Орг-методическая"

    ws.append(["Наименование", "Дата начала", "Дата окончания", "Отметка"])
    for w in works:
        ws.append([w.title, w.start_date, w.end_date, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="organizational.xlsx"'
    wb.save(response)
    return response


@login_required
def export_research_excel(request):
    teacher = request.user.teacher
    works = ResearchWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "НИР"

    ws.append(["Тема", "Дата начала", "Дата окончания", "Отметка"])
    for w in works:
        ws.append([w.topic, w.start_date, w.end_date, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="research.xlsx"'
    wb.save(response)
    return response

@login_required
def export_contract_excel(request):
    teacher = request.user.teacher
    works = ContractResearchWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Хоздоговорная НИР"

    ws.append(["Тема", "Должность", "Дата начала", "Дата окончания", "Отметка"])
    for w in works:
        ws.append([w.topic, w.position, w.start_date, w.end_date, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="contract.xlsx"'
    wb.save(response)
    return response


@login_required
def export_scientific_excel(request):
    teacher = request.user.teacher
    works = ScientificMethodicalWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Научно-методическая"

    ws.append(["Тема", "Дата начала", "Дата окончания", "Отметка"])
    for w in works:
        ws.append([w.topic, w.start_date, w.end_date, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="scientific.xlsx"'
    wb.save(response)
    return response


@login_required
def export_social_excel(request):
    teacher = request.user.teacher
    works = SocialEducationalWork.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Общественная работа"

    ws.append(["Наименование", "Отметка"])
    for w in works:
        ws.append([w.title, w.completed])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="social.xlsx"'
    wb.save(response)
    return response


@login_required
def export_remarks_excel(request):
    teacher = request.user.teacher
    works = TeacherRemark.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Замечания"

    ws.append(["Дата", "Содержание"])
    for w in works:
        ws.append([w.date, w.content])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="remarks.xlsx"'
    wb.save(response)
    return response


@login_required
def export_qualification_excel(request):
    teacher = request.user.teacher
    works = QualificationUpgrade.objects.filter(teacher=teacher)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Повышение квалификации"

    ws.append(["Название", "Место", "Номер документа", "Дата", "Срок", "Объём"])
    for w in works:
        ws.append([w.title, w.location, w.document_number, w.date, w.duration, w.volume])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="qualification.xlsx"'
    wb.save(response)
    return response


from django.db.models import Model

def has_academic_year_field(model: Model):
    return 'academic_year' in [f.name for f in model._meta.fields]

def export_full_teacher_excel(request):
    teacher = request.user.teacher
    selected_year = request.GET.get("year") or request.session.get("selected_year")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    def add_sheet(title, model_cls, columns, extract_fn):
        ws = wb.create_sheet(title=title)
        ws.append(columns)

        qs = model_cls.objects.filter(teacher=teacher)
        if selected_year and has_academic_year_field(model_cls):
            qs = qs.filter(academic_year=selected_year)

        for obj in qs:
            ws.append(extract_fn(obj))

        for col in range(1, len(columns) + 1):
            ws.column_dimensions[get_column_letter(col)].width = 20

    add_sheet("Уч.-методическая", EducationalMethodicalWork,
              ["Название", "Начало", "Окончание", "Отметка", "Год"],
              lambda w: [w.title, w.start_date, w.end_date, w.completed, w.academic_year])

    add_sheet("Орг.-методическая", OrganizationalMethodicalWork,
              ["Название", "Начало", "Окончание", "Отметка"],
              lambda w: [w.title, w.start_date, w.end_date, w.completed])

    add_sheet("НИР", ResearchWork,
              ["Тема", "Начало", "Окончание", "Отметка"],
              lambda w: [w.topic, w.start_date, w.end_date, w.completed])

    add_sheet("Хоздоговорная", ContractResearchWork,
              ["Тема", "Должность", "Начало", "Окончание", "Отметка"],
              lambda w: [w.topic, w.position, w.start_date, w.end_date, w.completed])

    add_sheet("Научно-методическая", ScientificMethodicalWork,
              ["Тема", "Начало", "Окончание", "Отметка"],
              lambda w: [w.topic, w.start_date, w.end_date, w.completed])

    add_sheet("Общественная работа", SocialEducationalWork,
              ["Наименование", "Отметка"],
              lambda w: [w.title, w.completed])

    add_sheet("Замечания", TeacherRemark,
              ["Дата", "Содержание"],
              lambda w: [w.date, w.content])

    add_sheet("Повышение квалификации", QualificationUpgrade,
              ["Название", "Место", "Номер документа", "Дата", "Срок", "Объём"],
              lambda w: [w.title, w.location, w.document_number, w.date, w.duration, w.volume])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f'teacher_full_report_{selected_year or "all"}.xlsx'
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def teacher_profile(request):
    teacher = request.user.teacher
    return render(request, 'main/teacher_profile.html', {'teacher': teacher})