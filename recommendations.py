def get_recommendations(background, goals, electives):
    recommendations = []
    tech_keywords = ['программирование', 'разработка', 'архитектура', 'devops', 'алгоритмы', 'deep learning', 'computer vision', 'mle', 'backend', 'микросервисов', 'инженерия данных']
    product_keywords = ['продукт', 'менеджмент', 'управление', 'дизайн', 'экономика', 'стартап', 'аналитика', 'маркетинг', 'бизнес-планирование', 'фандрайзинг']
    research_keywords = ['исследовани', 'научн', 'семинар', 'моделирование', 'академическое письмо']
    if goals == 'product':
        for course in electives:
            if any(kw in course.lower() for kw in product_keywords): recommendations.append(f"- {course} (для развития продуктовых навыков)")
    if goals == 'tech':
        for course in electives:
            if any(kw in course.lower() for kw in tech_keywords): recommendations.append(f"- {course} (для углубления технических знаний)")
    if goals == 'research':
        for course in electives:
            if any(kw in course.lower() for kw in research_keywords): recommendations.append(f"- {course} (для построения академической карьеры)")
    if background == 'weak_programming' and goals != 'product':
         for course in electives:
            if "программирования" in course.lower() or "алгоритмы" in course.lower() or "python" in course.lower(): recommendations.append(f"- {course} (чтобы усилить базу в программировании)")
    if not recommendations: return "На основе ваших ответов сложно дать однозначную рекомендацию. Советую ознакомиться со всем списком элективов и выбрать то, что вам наиболее интересно."
    return "Основываясь на ваших ответах, я бы порекомендовал обратить внимание на следующие дисциплины:\n" + "\n".join(sorted(list(set(recommendations))))
