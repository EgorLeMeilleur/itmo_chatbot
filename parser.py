import re
import time
import subprocess
import os
import pdfplumber
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_pdf_with_selenium(page_url, download_dir):
    """
    Использует Selenium для клика по кнопке и скачивания PDF, полностью подавляя логи.
    """
    # 1. Настройка опций браузера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Настройка папки для скачивания
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)

    # 2. ИСПРАВЛЕНИЕ: Настройка сервиса драйвера для полного подавления вывода
    # Это самый надежный способ убрать ВСЕ системные сообщения
    service = Service(
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    driver = None
    try:
        # 3. Запуск драйвера с полностью "тихими" настройками
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(page_url)
        wait = WebDriverWait(driver, 20)
        
        try:
            print("-> Ищу баннер cookies...")
            cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Принять')]")))
            print("-> Баннер найден, принимаю условия.")
            cookie_button.click()
            time.sleep(1)
        except Exception:
            print("-> Баннер cookies не найден или уже принят. Продолжаю.")

        print("-> Ищу кнопку 'Скачать учебный план'...")
        download_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Скачать учебный план')]")))
        
        print("-> Кнопка найдена. Прокручиваю страницу к кнопке...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", download_button)
        time.sleep(1)

        print("-> Кликаю на кнопку с помощью JavaScript...")
        driver.execute_script("arguments[0].click();", download_button)
        
        print("-> Ожидаю завершения скачивания файла...")
        seconds_waited = 0
        download_timeout = 60
        
        while seconds_waited < download_timeout:
            pdf_files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]
            crdownload_files = [f for f in os.listdir(download_dir) if f.endswith('.crdownload')]
            
            if pdf_files and not crdownload_files:
                time.sleep(2)
                downloaded_file_path = os.path.join(download_dir, pdf_files[0])
                print(f"-> Файл успешно скачан: {os.path.basename(downloaded_file_path)}")
                return downloaded_file_path

            time.sleep(1)
            seconds_waited += 1
            
        print("! Ошибка: Время ожидания скачивания истекло.")
        return None

    except Exception as e:
        print(f"! Критическая ошибка во время работы Selenium: {e}")
        return None
    finally:
        if driver:
            driver.quit()

# Остальные блоки кода остаются без изменений
def parse_pdf_curriculum_by_text(pdf_path, program_title):
    core_courses = []; elective_courses = []
    in_core_section = False; in_elective_section = False
    CORE_START_KEYWORDS = ["Обязательные дисциплины"]
    ELECTIVE_START_KEYWORDS = ["Пул выборных дисциплин", "Факультативные модули"]
    STOP_KEYWORDS = ["Блок 2. Практика", "Блок 3. ГИА", "Универсальная (надпрофессиональная) подготовка", "Иностранный язык", "Элективные микромодули Soft Skills"]
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if not text: continue
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if any(stop_word in line for stop_word in STOP_KEYWORDS): in_core_section=False; in_elective_section=False; continue
                    if any(start_word in line for start_word in CORE_START_KEYWORDS): in_core_section=True; in_elective_section=False; continue
                    if any(start_word in line for start_word in ELECTIVE_START_KEYWORDS): in_core_section=False; in_elective_section=True; continue
                    if in_core_section or in_elective_section:
                        if not line or "Наименование" in line or "Семестры" in line or not re.search('[а-яА-Я]', line): continue
                        course_name = re.sub(r'^\d(\s*,\s*\d)*\s*', '', line).strip()
                        if len(course_name.split()) < 2: continue
                        if in_core_section: core_courses.append(course_name)
                        elif in_elective_section: elective_courses.append(course_name)
        return {"title": program_title, "core_courses": sorted(list(set(c for c in core_courses if c))), "elective_courses": sorted(list(set(e for e in elective_courses if e)))}
    except Exception as e: print(f"Критическая ошибка при парсинге PDF файла {pdf_path}: {e}"); return None
