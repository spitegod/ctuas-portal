import os
import django
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


from main.models import Recommendation



def parse_methodical_work(sheet, teacher=None):
    for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        recommendation = row[0]


        Recommendation.objects.create(
            recommendation=recommendation.strip(),

        )

        print(f"[{i}] {recommendation.strip()} — добавлено")
