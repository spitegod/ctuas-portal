import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import Raising



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=2):
        date = row[0]
        form = row[1]
        mark = row[2]

        Raising.objects.create(
            date=str(date).strip() if date else "",
            form=form.strip(),
            mark=str(mark).strip() if mark else "",
        )

        print(f"[{i}] {form.strip()} — добавлено")
