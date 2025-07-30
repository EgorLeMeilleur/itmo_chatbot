import os
from parser import parse_pdf_curriculum_by_text, download_pdf_with_selenium
from chatbot import ChatBot

def main():
    print("🤖 Загружаю актуальные учебные планы с сайта ИТМО...")
    download_directory = os.path.join(os.getcwd(), "downloads")
    programs = [{"key": "ai", "title": "Искусственный интеллект", "page_url": "https://abit.itmo.ru/program/master/ai"}, {"key": "product", "title": "Управление ИИ-продуктами", "page_url": "https://abit.itmo.ru/program/master/ai_product"}]
    all_programs_data = []
    for program in programs:
        print(f"\n-> Обрабатываю программу «{program['title']}»...")
        downloaded_pdf_path = download_pdf_with_selenium(program['page_url'], download_directory)
        if not downloaded_pdf_path: all_programs_data.append(None); continue
        print(f"-> Парсю учебный план...")
        data = parse_pdf_curriculum_by_text(downloaded_pdf_path, program['title'])
        all_programs_data.append(data)
        os.remove(downloaded_pdf_path)
    if os.path.exists(download_directory) and not os.listdir(download_directory): os.rmdir(download_directory)

    if any(data is None or not data.get('core_courses') for data in all_programs_data):
        print("\nКритическая ошибка: не удалось загрузить или разобрать данные одной или нескольких программ. Бот не может продолжить работу.")
        return

    print("\n🤖 Данные успешно загружены!")
    bot = ChatBot(all_programs_data)
    bot.show_welcome_message()
    while True:
        try:
            user_input = input("\nВаш вопрос: ")
            if not bot.handle_command(user_input): print("\n🤖 До свидания! Удачи с поступлением!"); break
        except (KeyboardInterrupt, EOFError):
            print("\n\n🤖 Получена команда на завершение. До свидания!"); break

if __name__ == "__main__":
    main()