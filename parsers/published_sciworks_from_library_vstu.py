from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
import re

from main.models import Teacher, PublishedSciWork

def import_published_from_library(teacher, year_from="2024", year_to="2025"):
    search_name = get_short_name(teacher)

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://library.vstu.ru/publ_2/index.php?command=search2")
        
        driver.find_element(By.NAME, "fio").send_keys(search_name)
        driver.find_element(By.NAME, "year_rel1").send_keys(year_from)
        driver.find_element(By.NAME, "year_rel2").send_keys(year_to)

        driver.find_element(By.XPATH, "//input[@type='submit' and @value='Найти']").click()
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results_div = soup.find("div", class_="resultlist", id="LIST")
        if not results_div:
            return 0

        count = 0
        for p in results_div.find_all("p"):
            text = p.get_text().strip()
            if not text or len(text) < 10:
                continue

            # Полный текст публикации
            full_text = text

            # Разбиваем по " / "
            parts = text.split(" / ")
            if len(parts) < 2:
                continue

            # Название работы — первая часть (после номера с точкой)
            # Уберём номер и точку с начала
            name_part = re.sub(r'^\d+\.\s*[^,]+,\s*[^.]+\.\s*(?:[^.]+\.\s*)?', '', parts[0]).strip()

            name = name_part

            # Соавторы — часть между " / " и "//"
            autors = parts[1].split("//")[0].strip()

            # Объем — ищем в тексте, например "C. 410-411" или "6 п.л."
            size_match = re.search(r'(C\.\s*\d+[-–]?\d*)|(\d+\s*п\.л\.)', text)
            size = size_match.group(0) if size_match else ""

            # Вид работы — если есть логика, можно добавить, пока пусто
            type_work = ""

            # Проверяем, чтобы не дублировать по полю text
            if PublishedSciWork.objects.filter(teacher=teacher, output=full_text).exists():
                continue

            PublishedSciWork.objects.create(
                teacher=teacher,
                title=name,
                output=full_text,
                size=size,
                autors=autors
            )
            count += 1

        return count

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