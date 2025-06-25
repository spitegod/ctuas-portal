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

