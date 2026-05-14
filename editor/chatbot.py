"""
Чат-бот для помощи в обучении веб-программированию.
Отвечает на вопросы, даёт подсказки по заданиям и объясняет ошибки.
При наличии OPENAI_API_KEY в настройках использует модель OpenAI, иначе — локальные шаблоны.
"""
import logging
import re
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)

_MAX_CTX = 12000


def _truncate(text: Optional[str], limit: int = _MAX_CTX) -> str:
    if not text:
        return ''
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 20] + '\n… [обрезано]'


def _openai_reply(
    message: str,
    html: Optional[str],
    css: Optional[str],
    js: Optional[str],
    errors: Optional[list],
) -> Optional[str]:
    key = getattr(settings, 'OPENAI_API_KEY', '') or ''
    if not key:
        return None
    try:
        from openai import OpenAI
    except ImportError:
        logger.warning('Пакет openai не установлен, ответы без ИИ.')
        return None

    model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')
    err_lines = []
    if errors:
        for e in errors[:12]:
            err_lines.append(
                f"- {e.get('type', '?')}: строка {e.get('line', '?')}: {e.get('message', '')}"
            )
    errors_block = '\n'.join(err_lines) if err_lines else '(нет)'

    user_block = (
        f"Вопрос ученика:\n{message}\n\n"
        f"--- HTML ---\n{_truncate(html or '')}\n\n"
        f"--- CSS ---\n{_truncate(css or '')}\n\n"
        f"--- JavaScript ---\n{_truncate(js or '')}\n\n"
        f"--- Ошибки валидатора ---\n{errors_block}"
    )

    system = (
        'Ты дружелюбный преподаватель веб-разработки в проекте WebLearn. '
        'Отвечай по-русски, кратко и по делу. Помогай с HTML, CSS и JavaScript. '
        'Не выдавай готовые решения целиком, если это учебное задание — подсказывай шаги. '
        'Если есть ошибки валидатора, объясни, как их исправить. '
        'Код форматируй в блоках с указанием языка при необходимости.'
    )

    try:
        client = OpenAI(api_key=key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': user_block},
            ],
            max_tokens=2000,
            temperature=0.5,
        )
        text = (completion.choices[0].message.content or '').strip()
        return text if text else None
    except Exception as e:
        logger.warning('OpenAI недоступен: %s', e)
        return None


# База знаний: порядок важен — сначала частные шаблоны, общие (подсказк/помоги) в конце списка
HELP_RESPONSES = [
    # HTML — ссылки (частый вопрос)
    (
        r'ссылк|href|\b<a\b|как добавить ссыл|гиперссыл',
        "Ссылка в HTML — тег `<a>` (anchor):\n\n"
        "```html\n<a href=\"https://example.com\">Текст ссылки</a>\n```\n\n"
        "• `href` — адрес страницы.\n"
        "• Открыть в новой вкладке: `<a href=\"...\" target=\"_blank\" rel=\"noopener\">`.\n"
        "• Внутренняя ссылка по странице: `<a href=\"#раздел\">` и у блока `id=\"раздел\"`.\n\n"
        "Не забудьте закрыть тег: `</a>`."
    ),
    (
        r'научиться.*css|учиться.*css|писать.*на\s*css|изучить\s*css|как.*\bcss\b|основы\s*css',
        "Чтобы освоить CSS, идите от простого к сложному:\n\n"
        "1. **Синтаксис:** `селектор { свойство: значение; }`\n"
        "2. **Селекторы:** по тегу (`p`), классу (`.block`), id (`#main`).\n"
        "3. **Текст и цвет:** `color`, `font-size`, `font-family`.\n"
        "4. **Блок:** `margin`, `padding`, `width`, `height`, `border`.\n"
        "5. **Flexbox** — выравнивание в ряд/колонку: `display: flex`.\n\n"
        "В нашем редакторе откройте вкладку CSS и меняйте стили — превью обновляется сразу. "
        "Попробуйте задать цвет заголовку: `h1 { color: #6366f1; }`."
    ),
    (
        r'строк[еуи]\s*\d+|строка\s*\d+|в строке\s*\d+',
        "Чтобы разобрать ошибку «в строке N», откройте панель «Ошибки» под редактором — там тип файла (HTML/CSS/JS) и номер строки.\n\n"
        "Перейдите на нужную вкладку, найдите эту строку в коде. Часто это незакрытая скобка, кавычка или тег. "
        "Если пришлёте текст ошибки из панели целиком — подскажу точнее."
    ),
    # HTML
    (
        r'\bhtml\b.*\bтег\b|тег.*html|как создать (страницу|страницу html)',
        "Для создания HTML-страницы начните с базовой структуры:\n\n"
        "```html\n<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Заголовок</title>\n</head>\n<body>\n  <!-- Ваш контент -->\n</body>\n</html>\n```\n\n"
        "Все парные теги нужно закрывать: <div>...</div>, <p>...</p>. Одиночные теги (img, br, input) закрывать не нужно."
    ),
    (
        r'<div\b|\bdiv\b|блок|контейнер',
        "Тег `<div>` — универсальный блочный контейнер. Используйте его для группировки элементов.\n\n"
        "Пример: `<div class=\"container\"><p>Текст</p></div>`\n\n"
        "Не забудьте закрыть тег: `</div>`"
    ),
    (
        r'не закрыт|не закрытый|unclosed|забыл закрыть',
        "Ошибка «тег не закрыт» означает, что вы открыли парный тег (например, <div> или <p>), но не добавили закрывающий </div> или </p>.\n\n"
        "Проверьте все открывающие теги и убедитесь, что у каждого есть пара. Вложенность должна соблюдаться: если открыли <div>, затем <p>, закрывайте сначала </p>, потом </div>."
    ),
    (
        r'вложенность|nesting|не тот тег',
        "Нарушение вложенности — когда закрывающий тег не соответствует последнему открытому. Например:\n"
        "❌ `<div><p></div></p>` — неправильно\n"
        "✅ `<div><p></p></div>` — правильно\n\n"
        "Закрывайте теги в обратном порядке их открытия."
    ),
    (
        r'\bcss\b.*(подключить|добавить|как)|как (подключить|добавить) css',
        "CSS можно добавить тремя способами:\n\n"
        "1. Внутри <head>: `<style>селектор { свойство: значение; }</style>`\n"
        "2. Внешний файл: `<link rel=\"stylesheet\" href=\"style.css\">`\n"
        "3. В нашем редакторе — вкладка CSS уже подключается к странице автоматически."
    ),
    (
        r'селектор|selector|\bclass\b|\bid\b',
        "Селекторы CSS:\n"
        "• `.class` — элементы с классом: `<div class=\"box\">` → `.box { }`\n"
        "• `#id` — элемент с id: `<p id=\"main\">` → `#main { }`\n"
        "• `элемент` — по тегу: `p { }` для всех <p>\n\n"
        "В CSS не забудьте закрыть фигурные скобки `{ }`."
    ),
    (
        r'скобк|кавычк|bracket|quote',
        "Частые ошибки со скобками и кавычками:\n\n"
        "• В CSS: каждое свойство заканчивается точкой с запятой `;`, блок — фигурными скобками `{ }`\n"
        "• В JS: круглые `()`, квадратные `[]`, фигурные `{}` должны быть сбалансированы\n"
        "• Кавычки \" и ' должны иметь пару. Если строка начинается с \", она должна заканчиваться \""
    ),
    (
        r'javascript|\bjs\b|скрипт',
        "JavaScript добавляется через тег <script> или во вкладке JS редактора.\n\n"
        "Базовый пример:\n```javascript\ndocument.addEventListener('DOMContentLoaded', function() {\n  // код после загрузки страницы\n});\n```\n\n"
        "Проверьте: все скобки (), [], {} должны быть сбалансированы."
    ),
    (
        r'ошибк|не работает|что не так|\berror\b',
        "Посмотрите панель «Ошибки» под редактором — там показаны проблемы с разметкой, стилями и скриптами.\n\n"
        "Типичные причины:\n"
        "• Незакрытые теги в HTML\n"
        "• Незакрытые скобки в CSS или JS\n"
        "• Опечатка в имени тега или свойства\n\n"
        "Напишите мне конкретную ошибку или выделенный текст — подскажу, как исправить."
    ),
    (
        r'привет|здравствуй|начать|start',
        "Привет! Я помощник WebLearn. Могу ответить на вопросы по HTML, CSS и JavaScript, "
        "дать подсказки по заданиям и объяснить ошибки в коде.\n\n"
        "Напишите свой вопрос или вставьте фрагмент кода с ошибкой."
    ),
    (
        r'подсказк|hint|помоги|как сделать|не понимаю',
        "Я могу помочь с HTML, CSS и JavaScript. Задайте конкретный вопрос, например:\n"
        "• «Как добавить ссылку?»\n"
        "• «Почему не закрыт тег?»\n"
        "• «Как изменить цвет текста в CSS?»\n"
        "• «Объясни эту ошибку» (пришлите текст ошибки)\n\n"
        "Также можете отправить свой код — я проанализирую его и подскажу."
    ),
]


def _match_response(text: str) -> Optional[str]:
    """Находит подходящий ответ по ключевым словам."""
    text_lower = text.lower().strip()
    for pattern, response in HELP_RESPONSES:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return response
    return None


def _analyze_code_errors(errors: list) -> str:
    """Формирует пояснение по списку ошибок."""
    if not errors:
        return ""
    parts = []
    for e in errors[:5]:  # макс 5 ошибок
        msg = e.get('message', '')
        hint = e.get('hint', '')
        code_type = e.get('type', '')
        line = e.get('line', 0)
        parts.append(f"• Строка {line}: {msg}")
        if hint:
            parts.append(f"  Подсказка: {hint}")
    return "\n".join(parts)


def get_chat_response(
    message: str,
    html: Optional[str] = None,
    css: Optional[str] = None,
    js: Optional[str] = None,
    errors: Optional[list] = None
) -> str:
    """
    Генерирует ответ чат-бота на сообщение пользователя.
    
    :param message: Вопрос пользователя
    :param html: Текущий HTML-код (для контекста)
    :param css: Текущий CSS-код
    :param js: Текущий JS-код
    :param errors: Список ошибок из валидатора
    """
    msg = message.strip()
    if not msg:
        return "Напишите ваш вопрос или опишите проблему."

    ai = _openai_reply(msg, html, css, js, errors)
    if ai:
        return ai
    
    # Если пользователь спрашивает про ошибки и переданы ошибки
    if errors and any(kw in msg.lower() for kw in ['ошибк', 'error', 'почему', 'исправить', 'что не так']):
        analysis = _analyze_code_errors(errors)
        if analysis:
            return (
                "Вот что я нашёл в вашем коде:\n\n" + analysis + "\n\n"
                "Исправьте отмеченные места и проверьте снова. Если нужны подробности — спросите про конкретную строку."
            )
    
    # Поиск по базе знаний
    response = _match_response(msg)
    if response:
        return response
    
    # Универсальный ответ
    return (
        "Попробуйте задать вопрос более конкретно. Например:\n"
        "• «Как добавить ссылку в HTML?»\n"
        "• «Объясни ошибку в строке 5»\n"
        "• «Как задать цвет фона в CSS?»\n\n"
        "Или скопируйте текст ошибки из панели — я помогу его разобрать."
    )
