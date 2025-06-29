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