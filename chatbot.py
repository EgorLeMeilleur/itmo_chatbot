from recommendations import get_recommendations

class ChatBot:
    def __init__(self, programs_data): self.programs = {"ai": programs_data[0], "product": programs_data[1]}
    def handle_command(self, command):
        command = command.lower().strip()
        if "привет" in command: self.show_welcome_message()
        elif "сравн" in command: self.compare_programs()
        elif "расскажи про ai" in command or "искусственный интеллект" in command: self.describe_program("ai")
        elif "расскажи про продукт" in command or "продуктовый" in command: self.describe_program("product")
        elif "посоветуй" in command or "рекоменд" in command: self.initiate_recommendation_flow()
        elif "пока" in command or "выход" in command: return False
        else: print("\n🤖 Я не совсем понял ваш вопрос. Попробуйте использовать одну из команд:\n- 'сравни программы'\n- 'расскажи про ai'\n- 'расскажи про продуктовый ии'\n- 'посоветуй курсы'\n- 'выход'")
        return True
    def show_welcome_message(self): print(f"\n🤖 Здравствуйте! Я чат-бот, который поможет вам выбрать между двумя магистерскими программами в ИТМО:\n1. {self.programs['ai']['title']}\n2. {self.programs['product']['title']}\n\nЗадайте мне вопрос, например: 'сравни программы' или 'посоветуй курсы'.")
    def describe_program(self, key):
        program = self.programs.get(key)
        if not program: print("Такая программа не найдена."); return
        print(f"\n--- Учебный план программы «{program['title']}» ---")
        print("\nОбязательные дисциплины:"); [print(f"- {c}") for c in program['core_courses']] if program['core_courses'] else print("Не найдены.")
        print("\nДисциплины по выбору:"); [print(f"- {e}") for e in program['elective_courses']] if program['elective_courses'] else print("Не найдены.")
    def compare_programs(self):
        ai, product = self.programs['ai'], self.programs['product']
        print("\n--- Сравнение обязательных дисциплин ---")
        ai_core, product_core = set(ai['core_courses']), set(product['core_courses'])
        common_core = ai_core.intersection(product_core); unique_to_ai = ai_core.difference(product_core); unique_to_product = product_core.difference(ai_core)
        print(f"\nОбщие обязательные дисциплины для обеих программ:"); [print(f"- {c}") for c in sorted(list(common_core))] if common_core else print("Не найдено.")
        print(f"\nУникальные обязательные дисциплины для «{ai['title']}»:"); [print(f"- {c}") for c in sorted(list(unique_to_ai))] if unique_to_ai else print("Не найдено.")
        print(f"\nУникальные обязательные дисциплины для «{product['title']}»:"); [print(f"- {c}") for c in sorted(list(unique_to_product))] if unique_to_product else print("Не найдено.")
        print("\nОсновное различие: программа 'Искусственный интеллект' больше сфокусирована на фундаментальных и исследовательских аспектах ИИ, в то время как 'Продуктовый ИИ' делает акцент на управлении, внедрении и коммерциализации ИИ-решений.")
    def initiate_recommendation_flow(self):
        print("\n🤖 Чтобы дать рекомендацию, мне нужно больше узнать о вас.")
        while True:
            bg_choice = input("Оцените свой уровень программирования:\n1. Сильный (уверенно пишу код)\n2. Слабый (нужно подтянуть)\nВаш выбор (1/2): ").strip()
            if bg_choice in ['1', '2']: background = 'strong_programming' if bg_choice == '1' else 'weak_programming'; break
            else: print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
        while True:
            goal_choice = input("\nЧто вам интереснее?\n1. Техническое развитие (ML-инженер, разработчик)\n2. Продуктовое развитие (продакт-менеджер, управление)\n3. Научная карьера (исследования, аспирантура)\nВаш выбор (1/2/3): ").strip()
            if goal_choice in ['1', '2', '3']: goals = {'1': 'tech', '2': 'product', '3': 'research'}[goal_choice]; break
            else: print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")
        while True:
            program_choice = input(f"\nДля какой программы сделать рекомендацию по элективам?\n1. {self.programs['ai']['title']}\n2. {self.programs['product']['title']}\nВаш выбор (1/2): ").strip()
            if program_choice in ['1', '2']: electives = self.programs['ai']['elective_courses'] if program_choice == '1' else self.programs['product']['elective_courses']; break
            else: print("Некорректный ввод. Пожалуйста, введите 1 или 2.")
        print(f"\n--- Ваши персональные рекомендации ---\n{get_recommendations(background, goals, electives)}")