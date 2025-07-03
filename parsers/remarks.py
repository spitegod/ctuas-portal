import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import Remark



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=2):
        date = row[0]
        remark = row[1]
        signature = row[2]

        Remark.objects.create(
            date=str(date).strip() if date else "",
            remark=remark.strip(),
            signature=str(signature).strip() if signature else "",
        )

        print(f"[{i}] {remark.strip()} — добавлено")
