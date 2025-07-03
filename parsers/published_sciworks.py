import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import SciMethodicalWork



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=2):
        n = row[0]
        name = row[1]
        output = row[2]
        vol = row[3]
        coauthor = row[4] if len(row) > 4 else ""


        if not name or str(name).strip() == "":
            continue

        SciMethodicalWork.objects.create(
            n=n.strip(),
            name=name.strip(),
            output=output.strip(),
            vol=vol.strip(),
            coauthor=coauthor.strip(),
        )

        print(f"[{i}] {name.strip()} — добавлено")
