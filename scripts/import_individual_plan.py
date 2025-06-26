import os
import django
import openpyxl
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from main.models import DisciplineLoad

def float_or_none(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def import_discipline_load(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.active

    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=3):
        discipline = row[0]
        if not discipline:
            continue  # пропускаем пустые строки

        total_plan = sum(filter(None, [
            float_or_none(row[4]), float_or_none(row[5]), float_or_none(row[6]),
            float_or_none(row[7]), float_or_none(row[8]), float_or_none(row[9]),
            float_or_none(row[10]), float_or_none(row[11]), float_or_none(row[12]),
            float_or_none(row[13]), float_or_none(row[14]), float_or_none(row[15]),
            float_or_none(row[16]), float_or_none(row[17]), float_or_none(row[18]),
            float_or_none(row[19])
        ]))

        DisciplineLoad.objects.create(
            discipline=discipline,
            course=row[1],
            group_count=row[2],
            student_count=row[3],
            lectures=float_or_none(row[4]),
            practicals=float_or_none(row[5]),
            labs=float_or_none(row[6]),
            project_work=float_or_none(row[7]),
            consultations=float_or_none(row[8]),
            tests=float_or_none(row[9]),
            exams=float_or_none(row[10]),
            review_distance=float_or_none(row[11]),
            practice_supervision=float_or_none(row[12]),
            visit_control=float_or_none(row[13]),
            qualification_supervision=float_or_none(row[14]),
            committee_work=float_or_none(row[15]),
            exam_commission=float_or_none(row[16]),
            phd_supervision=float_or_none(row[17]),
            org_srs=float_or_none(row[18]),
            rating=float_or_none(row[19]),
            total_plan=round(total_plan, 1),
            total_actual=float_or_none(row[21])
        )

        print(f"[{i}] {discipline} — добавлено")

if __name__ == '__main__':
    import_discipline_load("data/ip_test.xlsx")
