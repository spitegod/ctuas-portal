from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    TYPE_CHOICES = [
        ('Внутр', 'Внутр'),
        ('Шт', 'Шт'),
    ]

    full_name = models.CharField("ФИО", max_length=255)
    teacher_type = models.CharField("Тип", max_length=10, choices=TYPE_CHOICES)
    position = models.CharField("Должность", max_length=100)
    rate = models.CharField("Ставка", max_length=10)
    degree = models.CharField("Степень", max_length=100, blank=True, null=True)
    rank = models.CharField("Звание", max_length=100, blank=True, null=True)
    email = models.EmailField("Почта", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=50, blank=True, null=True)
    birthday = models.DateField("День рождения", blank=True, null=True)
    address = models.TextField("Домашний адрес", blank=True, null=True)

    # Привязка к учетной записи
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
# Create your models here.




class FirstSem(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name="first_sems")
    discipline = models.CharField(max_length=255)
    course = models.IntegerField(null=True, blank=True)
    group_count = models.IntegerField(null=True, blank=True)
    student_count = models.IntegerField(null=True, blank=True)

    lectures = models.FloatField(null=True, blank=True)
    practicals = models.FloatField(null=True, blank=True)
    labs = models.FloatField(null=True, blank=True)
    project_work = models.FloatField(null=True, blank=True)
    consultations = models.FloatField(null=True, blank=True)
    tests = models.FloatField(null=True, blank=True)
    exams = models.FloatField(null=True, blank=True)
    review_distance = models.FloatField(null=True, blank=True)
    practice_supervision = models.FloatField(null=True, blank=True)
    visit_control = models.FloatField(null=True, blank=True)
    qualification_supervision = models.FloatField(null=True, blank=True)
    committee_work = models.FloatField(null=True, blank=True)
    exam_commission = models.FloatField(null=True, blank=True)
    phd_supervision = models.FloatField(null=True, blank=True)
    org_srs = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    total_plan = models.FloatField(null=True, blank=True)
    total_actual = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.discipline} (курс {self.course})"


class SecondSem(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name="second_sems")
    discipline = models.CharField(max_length=255)
    course = models.IntegerField(null=True, blank=True)
    group_count = models.IntegerField(null=True, blank=True)
    student_count = models.IntegerField(null=True, blank=True)

    lectures = models.FloatField(null=True, blank=True)
    practicals = models.FloatField(null=True, blank=True)
    labs = models.FloatField(null=True, blank=True)
    project_work = models.FloatField(null=True, blank=True)
    consultations = models.FloatField(null=True, blank=True)
    tests = models.FloatField(null=True, blank=True)
    exams = models.FloatField(null=True, blank=True)
    review_distance = models.FloatField(null=True, blank=True)
    practice_supervision = models.FloatField(null=True, blank=True)
    visit_control = models.FloatField(null=True, blank=True)
    qualification_supervision = models.FloatField(null=True, blank=True)
    committee_work = models.FloatField(null=True, blank=True)
    exam_commission = models.FloatField(null=True, blank=True)
    phd_supervision = models.FloatField(null=True, blank=True)
    org_srs = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    total_plan = models.FloatField(null=True, blank=True)
    total_actual = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.discipline} (курс {self.course})"
    
class EducationalMethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='edu_methods')
    title = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100, blank=True, null=True)
    completed = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    academic_year = models.CharField("Учебный год", max_length=9, default="2024–2025")
     

    def __str__(self):
        return self.title
    
class OrganizationalMethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='org_methods')
    title = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100, blank=True, null=True)
    completed = models.CharField("Отметка о выполнении", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class ResearchWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='research_works')
    topic = models.TextField("Наименование темы, этап, задание")  # ← изменено название поля
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100, blank=True, null=True)
    completed = models.CharField("Отметка о выполнении", max_length=100, blank=True)

    def __str__(self):
        return self.topic
    
class ContractResearchWork(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    topic = models.TextField("Наименование темы, шифр")
    position = models.CharField("Должность по НИР", max_length=255)
    start_date = models.DateField("Начало")
    end_date = models.DateField("Окончание", null=True, blank=True)
    completed = models.CharField("Отметка о выполнении", max_length=255, blank=True)

    def __str__(self):
        return f"{self.topic} ({self.teacher})"
    
class ScientificMethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='scientific_methods')
    topic = models.TextField("Наименование темы, этап, задание")
    start_date = models.CharField("Начало", max_length=100)
    end_date = models.CharField("Окончание", max_length=100, blank=True, null=True)
    completed = models.CharField("Отметка о выполнении", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.topic
    
class MethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='methodical_works')
    name = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100)
    status = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.teacher.full_name})"

class OrgMethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='org_methodical_works')
    name = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100)
    status = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    
    
    def __str__(self):
        return f"{self.name} ({self.teacher.full_name})"


class SciResearchWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='sci_research_works')
    name = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100)
    status = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    
    def __str__(self):
     return f"{self.name} ({self.teacher.full_name})"


class ContractWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='contract_works')
    name = models.TextField("Наименование работы")
    job = models.TextField("Должность по НИР", max_length=100)
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100)
    status = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.teacher.full_name})"

class SciMethodicalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='sci_methodical_works')
    name = models.TextField("Наименование работы")
    start_date = models.CharField("Начало работы", max_length=100)
    end_date = models.CharField("Окончание работы", max_length=100)
    status = models.CharField("Отметка о выполнении", max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.teacher.full_name})"

class SocialEducationalWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='social_works')
    title = models.TextField("Наименование работы")
    completed = models.CharField("Отметка о выполнении", max_length=100, blank=True)

    def __str__(self):
        return self.title

class TeacherRemark(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='remarks')
    date = models.DateField("Дата")
    content = models.TextField("Содержание замечаний")

    def __str__(self):
        return f"{self.date} — {self.content[:30]}"
    

class QualificationUpgrade(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='qualifications')
    title = models.CharField("Название", max_length=255)
    location = models.CharField("Место", max_length=255)
    document_number = models.CharField("Номер документа", max_length=100)
    date = models.DateField("Дата")
    duration = models.CharField("Срок прохождения", max_length=100)
    volume = models.CharField("Объём", max_length=100)

    def __str__(self):
        return f"{self.title} ({self.date})"
    
class PublishedSciWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='published_sci_work')
    title = models.TextField("Наименование и вид работы", max_length=100)
    output = models.TextField("Выходные данные", max_length=100)
    size = models.TextField("Объем в п.л.", max_length=100)
    autors = models.TextField("Соавторы", max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.teacher.full_name})"

class PublicWork(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='public_works')
    name = models.TextField("Наименование работы")
    mark = models.TextField("Отметка о выполнении", max_length=100)
    
    
    def __str__(self):
        return f"{self.name} ({self.teacher.full_name})"


class Remark(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='remarks_manual')
    date = models.TextField("Дата")
    remark = models.TextField("Содержание замечаний", max_length=100)
    signature = models.TextField("Роспись проверяющего", max_length=100)
    
    def __str__(self):
        return f"{self.date} — {self.remark[:30]}"



class Raising(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='raising')
    date = models.TextField("Дата")
    form = models.TextField("Форма повышения квалификации", max_length=100)
    mark = models.TextField("Отметка о выполнении", max_length=100)
    
    def __str__(self):
        return f"{self.date} — {self.remark[:30]}"


class Recommendation(models.Model):
    teacher = models.ForeignKey('main.Teacher', on_delete=models.CASCADE, related_name='recommendation')
    recom = models.TextField("Рекомендация кафедры по избранию преподавателя")
       
    def __str__(self):
        return f"Рекомендация — {self.teacher.full_name}"
    
class TeacherPermission(models.Model):
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, related_name='permissions')
    can_manage_accounts = models.BooleanField("Может управлять пользователями", default=False)
    can_edit_ip = models.BooleanField("Может редактировать уровни доступа", default=False)
    can_edit_pps = models.BooleanField("Может редактировать ППС", default=False)

    def __str__(self):
        return f"Права для {self.teacher.full_name}"
    

class TeachingLoad(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    discipline = models.CharField(max_length=255)
    course = models.CharField(max_length=10)
    groups = models.CharField(max_length=100)
    students = models.IntegerField(default=0)
    lectures = models.FloatField(default=0)
    practice = models.FloatField(default=0)
    labs = models.FloatField(default=0)
    coursework = models.FloatField(default=0)
    consultations = models.FloatField(default=0)
    exams = models.FloatField(default=0)
    review_work = models.FloatField(default=0)
    practice_supervision = models.FloatField(default=0)
    thesis_supervision = models.FloatField(default=0)
    gak = models.FloatField(default=0)
    admission = models.FloatField(default=0)
    phd_supervision = models.FloatField(default=0)
    org_work = models.FloatField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.teacher.full_name} — {self.discipline}"

    @property
    def total_hours(self):
        return sum(filter(None, [
            self.lectures,
            self.practice,
            self.labs,
            self.coursework,
            self.consultations,
            self.exams,
            self.review_work,
            self.practice_supervision,
            self.org_work,
            self.thesis_supervision,
            self.gak,
            self.admission,
            self.phd_supervision,
        ]))
