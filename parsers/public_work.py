import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import PublicWork



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if not row or len(row) == 0:
            continue  # полностью пустая строка
        
        name = row[0]
        mark = row[1] if len(row) > 1 else ""

        if not name or str(name).strip() == "":
            continue

        PublicWork.objects.create(
            name=str(name).strip(),
            mark=str(mark).strip() if mark else ""
        )

        print(f"[{i}] {name.strip()} — добавлено")
