import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import SciMethodicalWork



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=2):
        name = row[0]
        start = row[1]
        end = row[2]
        status = row[3] if len(row) > 3 else ""


        if not name or str(name).strip() == "":
            continue

        SciMethodicalWork.objects.create(
            name=name.strip(),
            start_date=str(start).strip() if start else "",
            end_date=str(end).strip() if end else "",
            status=str(status).strip() if status else ""
        )

        print(f"[{i}] {name.strip()} — добавлено")
