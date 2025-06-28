import openpyxl
from main.models import Teacher
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='main_teacher';")
    
def import_teachers_from_excel(file_path):
    import openpyxl
    from main.models import Teacher

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    Teacher.objects.all().delete()
    

    for i, row in enumerate(sheet.iter_rows(min_row=2), start=2):
        try:
            first_cell = row[0].value
            if not first_cell or isinstance(first_cell, str) and "итого" in first_cell.lower():
                continue  # пропускаем пустые строки или строки с подытогами

            # Определяем, сдвинуты ли данные на 1 колонку (если нет номера строки)
            if isinstance(first_cell, int):  # обычная строка с номером
                full_name = row[1].value
                teacher_type = row[2].value
                position = row[3].value
                rate = row[4].value
                degree = row[5].value
                rank = row[6].value
                email = row[7].value
                phone = row[8].value
                birthday = row[9].value
                address = row[10].value
            else:  # сдвиг на 1 колонку (нет номера строки)
                full_name = row[0].value
                teacher_type = row[1].value
                position = row[2].value
                rate = row[3].value
                degree = row[4].value
                rank = row[5].value
                email = row[6].value
                phone = row[7].value
                birthday = row[8].value
                address = row[9].value

            if not full_name or not position or not rate:
                continue  # пропускаем, если нет ключевых данных

            Teacher.objects.create(
                full_name=full_name,
                teacher_type=teacher_type or "",
                position=position,
                rate=rate,
                degree=degree or "",
                rank=rank or "",
                email=email or "",
                phone=phone or "",
                birthday=birthday or None,
                address=address or ""
            )
            print(f"[{i}] {full_name} — добавлен")
        except Exception as e:
            print(f"[{i}] Ошибка: {e}")
