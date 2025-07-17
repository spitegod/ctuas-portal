from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re

from main.models import Teacher, PublishedSciWork

def import_published_from_library(teacher, year_from="2024", year_to="2025"):
    search_name = get_short_name(teacher)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://library.vstu.ru/publ_2/index.php?command=search2")
        
        driver.find_element(By.NAME, "fio").send_keys(search_name)
        driver.find_element(By.NAME, "year_rel1").send_keys(year_from)
        driver.find_element(By.NAME, "year_rel2").send_keys(year_to)

        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Найти']").click()

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results_div = soup.find("div", class_="resultlist", id="LIST")
        if not results_div:
            return 0

        count = 0
        for p in results_div.find_all("p"):
            text = p.get_text().strip()
            if not text:
                continue

            # Разбиваем по " / "
            parts = text.split(" / ")
            if len(parts) < 2:
                continue

            # Убираем номер в начале, например "10. "
            text_wo_number = re.sub(r'^\d+\.\s*', '', text)

            # Ищем позицию первого слэша " / ", чтобы разбить на части
            slash_pos = text_wo_number.find(" / ")
            if slash_pos == -1:
                continue

            # Всё, что до " / " — это потенциальное название (включая ФИО, которое мы хотим убрать)
            before_slash = text_wo_number[:slash_pos].strip()
            after_slash = text_wo_number[slash_pos + 3:].strip()  # После " / "

            # Удаляем возможные фамилии с инициалами в начале — "Фамилия, И.О."
            # Например: "Шлянников, В.М. Название работы"
            before_slash_cleaned = re.sub(r'^[А-ЯЁA-Z][^,]+,\s*[А-ЯA-Z]\.\s*(?:[А-ЯA-Z]\.\s*)?', '', before_slash).strip()

            # Название работы:
            title = before_slash_cleaned

            # Авторы — если после " / " и до "//" что-то есть
            autors = ""
            if "//" in after_slash:
                autors = after_slash.split("//")[0].strip()
            elif ";" in after_slash:
                autors = after_slash.split(";")[0].strip()

            # Выходные данные — всё после "//" или ";"
            output = ""
            if "//" in text:
                output = text.split("//", 1)[1].strip()
            elif ";" in text:
                output = text.split(";", 1)[1].strip()

            size = ""

            # 1. Диапазон страниц: "С. 348–349" или "P. 348–349"
            range_match = re.search(r'[СCПP]\.\s*(\d+)[–-](\d+)', text, re.IGNORECASE)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                pages = end - start + 1
                size = f"{pages}"

            # 2. Одна страница: "С. 408" или "P. 408"
            elif re.search(r'[СCПP]\.\s*\d+', text, re.IGNORECASE):
                size = "1"

            # 3. Количество страниц: "55 с." или "55 p."
            else:
                page_count_match = re.search(r'(\d+)\s*(?:с\.|p\.)', text, re.IGNORECASE)
                if page_count_match:
                    size = page_count_match.group(1)

            # Вид работы — если есть логика, можно добавить, пока пусто
            type_work = ""

            # Проверяем, чтобы не дублировать по полю text
            if PublishedSciWork.objects.filter(teacher=teacher, title=title).exists():
                continue

            PublishedSciWork.objects.create(
                teacher=teacher,
                title=title,
                output=output,
                size=size,
                autors=autors
            )
            count += 1

        return count

    except Exception as e:
        print(f"Ошибка при импорте: {e}")
        return -1, str(e)

    finally:
        driver.quit()


def get_short_name(teacher: Teacher) -> str:
    """
    Возвращает строку в формате Фамилия И.О.
    """
    parts = teacher.full_name.strip().split()
    if not parts:
        return ""

    last_name = parts[0]
    initials = ""

    if len(parts) > 1:
        initials += parts[1][0] + "."
    if len(parts) > 2:
        initials += parts[2][0] + "."

    return f"{last_name} {initials}"