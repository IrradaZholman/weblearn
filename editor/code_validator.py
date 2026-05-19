"""
Модуль проверки кода HTML, CSS и JavaScript.
Возвращает структурированные ошибки с пояснениями для отображения пользователю.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CodeError:
    """Ошибка в коде с метаданными."""
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    message: str = ""
    code: str = ""
    severity: str = "error"
    hint: str = ""


# HTML-теги, которые не требуют закрытия
HTML_VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr',
    'img', 'input', 'link', 'meta', 'param',
    'source', 'track', 'wbr'
}


def validate_html(code: str) -> List[CodeError]:
    """
    Проверка HTML:
    - незакрытые теги
    - неправильная вложенность
    - лишние закрывающие теги
    """

    errors: List[CodeError] = []
    lines = code.split('\n')

    stack: List[tuple] = []

    open_tag_re = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)(?:\s|>|/)')
    close_tag_re = re.compile(r'</([a-zA-Z][a-zA-Z0-9-]*)>')

    for line_num, line in enumerate(lines, 1):

        pos = 0

        while pos < len(line):

            open_match = open_tag_re.search(line, pos)
            close_match = close_tag_re.search(line, pos)

            next_open = open_match.start() if open_match else len(line)
            next_close = close_match.start() if close_match else len(line)

            # =========================================
            # ЗАКРЫВАЮЩИЙ ТЕГ
            # =========================================
            if next_close < next_open:

                if close_match:

                    tag = close_match.group(1).lower()
                    col = close_match.start()

                    # =====================================
                    # ЕСЛИ СТЕК ПУСТ
                    # =====================================
                    if not stack:

                        errors.append(CodeError(
                            line=line_num,
                            column=col,

                            message=f"Лишний тег </{tag}>",

                            code="unexpected-closing-tag",

                            hint=(
                                f"Удалите лишний тег </{tag}> "
                                f"или добавьте перед ним <{tag}>"
                            )
                        ))

                    else:

                        last_tag, last_line, last_col = stack[-1]

                        # =====================================
                        # НЕПРАВИЛЬНАЯ ВЛОЖЕННОСТЬ
                        # =====================================
                        if str(last_tag).lower().strip() != str(tag).lower().strip():

                            wrong_tag = last_tag

                            stack.pop()

                            errors.append(CodeError(
                                line=line_num,
                                column=col,

                                end_line=last_line,
                                end_column=last_col,

                                message=(
                                    f"Тег </{tag}> закрывает неправильный элемент."
                                ),

                                code="wrong-nesting",

                                hint=(
                                    f"Вы забыли закрыть тег </{wrong_tag}> "
                                    f"перед тегом </{tag}>."
                                )
                            ))

                        else:
                            stack.pop()

                    pos = close_match.end()

                else:
                    break

            # =========================================
            # ОТКРЫВАЮЩИЙ ТЕГ
            # =========================================
            else:

                if open_match:

                    tag = open_match.group(1).lower()
                    col = open_match.start()

                    full_tag_end = line.find('>', open_match.start())

                    if full_tag_end != -1:

                        tag_content = line[
                            open_match.start():full_tag_end + 1
                        ]

                        # <img />, <br />, <input />
                        if (
                            tag_content.rstrip().endswith('/>')
                            or tag in HTML_VOID_TAGS
                        ):
                            pos = full_tag_end + 1
                            continue

                    if tag not in HTML_VOID_TAGS:
                        stack.append((tag, line_num, col))

                    pos = open_match.end()

                else:
                    break

    # =========================================
    # НЕЗАКРЫТЫЕ ТЕГИ
    # =========================================
    for tag, ln, col in reversed(stack):

        errors.append(CodeError(
            line=ln,
            column=col,

            message=f"Тег <{tag}> не закрыт",

            code="unclosed-tag",

            hint=f"Добавьте закрывающий тег </{tag}>"
        ))

    return errors


def validate_css(code: str) -> List[CodeError]:
    """
    Проверка CSS:
    - незакрытые скобки
    - незакрытые кавычки
    """

    errors: List[CodeError] = []
    lines = code.split('\n')

    bracket_stack: List[tuple] = []

    in_string = None
    escape = False

    for line_num, line in enumerate(lines, 1):

        i = 0

        while i < len(line):

            ch = line[i]

            if escape:
                escape = False
                i += 1
                continue

            if ch == '\\' and in_string:
                escape = True
                i += 1
                continue

            if in_string:

                if ch == in_string:
                    in_string = None

                i += 1
                continue

            if ch in ('"', "'"):

                in_string = ch
                i += 1
                continue

            if ch == '{':

                bracket_stack.append((ch, line_num, i))

            elif ch == '}':

                if not bracket_stack:

                    errors.append(CodeError(
                        line=line_num,
                        column=i,

                        message="Лишняя закрывающая скобка }",

                        code="extra-brace",

                        hint="Удалите лишнюю }"
                    ))

                else:
                    bracket_stack.pop()

            i += 1

    if in_string:

        errors.append(CodeError(
            line=len(lines),
            column=0,

            message="Не закрыта кавычка",

            code="unclosed-quote",

            hint="Добавьте закрывающую кавычку"
        ))

    for char, ln, col in reversed(bracket_stack):

        errors.append(CodeError(
            line=ln,
            column=col,

            message="Вы забыли закрыть фигурную скобку }",

            code="unclosed-brace",

            hint="Добавьте закрывающую скобку }"
        ))

    return errors


def validate_javascript(code: str) -> List[CodeError]:
    """
    Базовая проверка JavaScript:
    - парность скобок
    - незакрытые строки
    """

    errors: List[CodeError] = []

    stack: List[tuple] = []

    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    opens = "([{"
    closes = ")]}"

    line_num = 1
    col = 0

    for ch in code:

        if ch == '\n':
            line_num += 1
            col = 0
            continue

        if ch in opens:
            stack.append((ch, line_num, col))

        elif ch in closes:

            if not stack:

                errors.append(CodeError(
                    line=line_num,
                    column=col,

                    message=f"Лишняя скобка {ch}",

                    code="extra-bracket",

                    hint="Удалите лишнюю скобку"
                ))

            else:

                last, ln, c = stack[-1]

                if last != pairs[ch]:

                    errors.append(CodeError(
                        line=line_num,
                        column=col,

                        message="Неправильная последовательность скобок",

                        code="mismatched-bracket",

                        hint="Проверьте парность скобок"
                    ))

                else:
                    stack.pop()

        col += 1

    for ch, ln, c in reversed(stack):

        close = {
            '(': ')',
            '[': ']',
            '{': '}'
        }[ch]

        errors.append(CodeError(
            line=ln,
            column=c,

            message=f"Вы забыли закрыть скобку {ch}",

            code="unclosed-bracket",

            hint=f"Добавьте {close}"
        ))

    return errors


def validate_all(html: str, css: str, js: str) -> dict:
    """
    Проверка всего кода.
    """

    return {
        'html': validate_html(html),
        'css': validate_css(css),
        'js': validate_javascript(js)
    }
