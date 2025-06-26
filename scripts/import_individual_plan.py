import os
import sys
import django
import openpyxl

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Импорт всех обработчиков
from parsers import sheet_parsers

def import_all_sheets(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)

    for sheet_name in wb.sheetnames:
        print(f"Обработка листа: {sheet_name}")
        if sheet_name in sheet_parsers:
            sheet = wb[sheet_name]
            try:
                sheet_parsers[sheet_name](sheet)
                print(f"Успешно обработан лист: {sheet_name}")
            except Exception as e:
                print(f"Ошибка в листе '{sheet_name}': {e}")
        else:
            print(f"⚠️ Нет обработчика для листа: {sheet_name} (пропущен)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Укажи путь к Excel-файлу:\nПример: python import_individual_plan.py data/plan.xlsx")
    else:
        import_all_sheets(sys.argv[1])