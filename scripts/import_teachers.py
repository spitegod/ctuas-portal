import openpyxl
from main.models import Teacher

def import_teachers_from_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    for i, row in enumerate(sheet.iter_rows(min_row=2), start=2): 
        try:
            full_name = row[0].value
            teacher_type = row[1].value
            position = row[2].value
            rate = row[3].value
            degree = row[4].value
            title = row[5].value    
            email = row[6].value
            phone = row[7].value
            birthday = row[8].value
            address = row[9].value

            Teacher.objects.create(
                full_name=full_name,
                teacher_type=teacher_type,
                position=position,
                rate=rate,
                degree=degree,
                title=title,   
                email=email,
                phone=phone,
                birthday=birthday,
                address=address
            )
            print(f"[{i}] {full_name} — добавлен")
        except Exception as e:
            print(f"[{i}] Ошибка: {e}")