import os
import sys
import django

# Путь до корня проекта (где лежит manage.py)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Указание settings-файла
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Инициализация Django
django.setup()



import pandas as pd
from main.models import TeachingLoad, Teacher
import openpyxl

def safe_num(value):
    try:
        return float(value) if value not in (None, '', '-') else 0
    except:
        return 

def safe_num(value):
    try:
        if value in (None, '', '-'):
            return 0
        return float(value)
    except:
        return 0


def parse_teaching_load(filepath):
    print("Запускается импорт нагрузки...")

    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except FileNotFoundError:
        print(f"❌ Файл не найден: {filepath}")
        return

    sheet = wb.active
    count = 0
    skipped = 0

    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        short_name = row[25]
        if not short_name or str(short_name).strip().lower() in ('(фио)', 'фио'):
            continue

        # Извлекаем фамилию
        surname = str(short_name).split()[0]

        teacher = Teacher.objects.filter(full_name__icontains=surname).first()
        if not teacher:
            print(f"Пропущено: преподаватель '{short_name}' не найден в базе.")
            skipped += 1
            continue

        try:
            TeachingLoad.objects.create(
                teacher=teacher,
                discipline=row[2],
                course=row[7],
                groups=row[15],
                students=safe_num(row[10]),
                lectures=safe_num(row[27]),
                practice=safe_num(row[28]),
                labs=safe_num(row[29]),
                coursework=safe_num(row[46]) + safe_num(row[47]),
                consultations=safe_num(row[41]) + safe_num(row[42]),
                exams=safe_num(row[40]),
                review_work=safe_num(row[44]) + safe_num(row[45]),
                practice_supervision=safe_num(row[48]),
                thesis_supervision=safe_num(row[50]) + safe_num(row[51]),
                gak=safe_num(row[52]) + safe_num(row[53]),
                admission=safe_num(row[43]),
                phd_supervision=safe_num(row[55]),
                org_work=safe_num(row[49]),
                rating=safe_num(row[58]),
            )
            count += 1
        except Exception as e:
            print(f"⚠️ Ошибка на строке {i}: {e}")
            skipped += 1

    print(f"✅ Импорт завершён. Добавлено: {count}, Пропущено: {skipped}")
    
if __name__ == "__main__":
    parse_teaching_load("data/teaching_load.xlsx")