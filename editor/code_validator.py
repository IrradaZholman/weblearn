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
    severity: str = "error"  # error | warning
    hint: str = ""  # Подсказка как исправить


# HTML-теги, которые не требуют закрытия (void elements)
HTML_VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}

# Теги с особыми правилами вложенности
HTML_BLOCK_TAGS = {
    'html', 'head', 'body', 'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'section', 'article', 'header', 'footer', 'nav', 'main',
    'aside', 'figure', 'figcaption', 'form', 'table', 'thead', 'tbody', 'tr', 'td', 'th'
}


def validate_html(code: str) -> List[CodeError]:
    """
    Проверка HTML: парные теги, вложенность, незакрытые теги.
    """
    errors: List[CodeError] = []
    lines = code.split('\n')
    
    # Стек для отслеживания вложенности
    stack: List[tuple] = []  # (tag_name, line, column)
    
    # Регулярки для поиска тегов
    open_tag_re = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)(?:\s|>|/)')
    close_tag_re = re.compile(r'</([a-zA-Z][a-zA-Z0-9-]*)>')
    # Самозакрывающиеся <tag />
    self_closing_re = re.compile(r'<([a-zA-Z][a-zA-Z0-9-]*)\s+[^>]*/>')
    
    for line_num, line in enumerate(lines, 1):
        pos = 0
        while pos < len(line):
            # Пропускаем содержимое внутри строк (кавычки)
            in_script = 'script' in ''.join(t[0] for t in stack).lower() if stack else False
            in_style = 'style' in ''.join(t[0] for t in stack).lower() if stack else False
            
            # Ищем открывающий тег
            open_match = open_tag_re.search(line, pos)
            close_match = close_tag_re.search(line, pos)
            
            # Определяем что раньше
            next_open = open_match.start() if open_match else len(line)
            next_close = close_match.start() if close_match else len(line)
            
            if next_close < next_open:
                # Сначала закрывающий тег
                if close_match:
                    tag = close_match.group(1).lower()
                    col = close_match.start()
                    if not stack:
                        errors.append(CodeError(
                            line=line_num, column=col,
                            message=f"Неожиданный закрывающий тег </{tag}> — не найдено соответствующего открывающего тега",
                            code="unexpected-closing-tag",
                            hint=f"Удалите лишний тег </{tag}> или добавьте перед ним открывающий <{tag}>"
                        ))
                    else:
                        last_tag, last_line, last_col = stack[-1]
                        if last_tag.lower() != tag:
                            errors.append(CodeError(
                                line=line_num, column=col,
                                end_line=last_line, end_column=last_col,
                                message=f"Нарушена вложенность: тег </{tag}> закрывает не тот элемент. Ожидался </{last_tag}>",
                                code="wrong-nesting",
                                hint=f"Закройте сначала тег <{last_tag}> (строка {last_line}), затем </{tag}>"
                            ))
                        else:
                            stack.pop()
                    pos = close_match.end()
                else:
                    break
            else:
                # Открывающий тег
                if open_match:
                    tag = open_match.group(1).lower()
                    col = open_match.start()
                    
                    # Проверяем самозакрывающийся вид <tag ... />
                    rest = line[open_match.end():open_match.end()+50]
                    if '/>' in rest and rest.index('/>') < (rest.find('>') if '>' in rest else 999):
                        pos = open_match.end() + rest.index('/>') + 2
                        continue
                    
                    # Проверяем закрытие тега в этой же строке <tag>...</tag>
                    full_tag_end = line.find('>', open_match.start())
                    if full_tag_end != -1:
                        tag_content = line[open_match.start():full_tag_end+1]
                        if tag_content.rstrip().endswith('/>') or tag in HTML_VOID_TAGS:
                            pos = full_tag_end + 1
                            continue
                    
                    if tag not in HTML_VOID_TAGS:
                        stack.append((tag, line_num, col))
                    pos = open_match.end()
                else:
                    break
    
    # Оставшиеся незакрытые теги
    for tag, ln, col in reversed(stack):
        errors.append(CodeError(
            line=ln, column=col,
            message=f"Тег <{tag}> не закрыт",
            code="unclosed-tag",
            hint=f"Добавьте закрывающий тег </{tag}>"
        ))
    
    return errors


def validate_css(code: str) -> List[CodeError]:
    """
    Проверка CSS: незакрытые скобки, кавычки, точки с запятой.
    """
    errors: List[CodeError] = []
    lines = code.split('\n')
    
    bracket_stack: List[tuple] = []  # (char, line, col)
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
            
            if ch in ('"', "'") and not in_string:
                in_string = ch
                i += 1
                continue
            
            if ch in '{}':
                if ch == '{':
                    bracket_stack.append((ch, line_num, i))
                else:
                    if not bracket_stack:
                        errors.append(CodeError(
                            line=line_num, column=i,
                            message="Лишняя закрывающая скобка }",
                            code="extra-brace",
                            hint="Удалите лишнюю } или проверьте парность скобок { }"
                        ))
                    elif bracket_stack[-1][0] != '{':
                        errors.append(CodeError(
                            line=line_num, column=i,
                            message="Неверная скобка — ожидалась другая",
                            code="mismatched-brace",
                            hint="Проверьте правильность расстановки скобок { }"
                        ))
                    else:
                        bracket_stack.pop()
                i += 1
                continue
            
            if ch in '()' and not in_string:
                if ch == '(':
                    bracket_stack.append((ch, line_num, i))
                else:
                    if bracket_stack and bracket_stack[-1][0] == '(':
                        bracket_stack.pop()
                    elif bracket_stack and bracket_stack[-1][0] != '(':
                        errors.append(CodeError(
                            line=line_num, column=i,
                            message="Лишняя закрывающая скобка )",
                            code="extra-paren",
                            hint="Проверьте парность скобок ( ) в функциях"
                        ))
            i += 1
    
    if in_string:
        errors.append(CodeError(
            line=len(lines), column=0,
            message="Не закрыта кавычка в строке",
            code="unclosed-quote",
            hint="Добавьте закрывающую кавычку \" или '"
        ))
    
    for char, ln, col in reversed(bracket_stack):
        if char == '{':
            errors.append(CodeError(
                line=ln, column=col,
                message="Не закрыта фигурная скобка {",
                code="unclosed-brace",
                hint="Добавьте закрывающую скобку } для селектора или блока"
            ))
        elif char == '(':
            errors.append(CodeError(
                line=ln, column=col,
                message="Не закрыта круглая скобка (",
                code="unclosed-paren",
                hint="Добавьте закрывающую скобку ) для функции"
            ))
    
    return errors


def validate_javascript(code: str) -> List[CodeError]:
    """
    Базовая проверка JavaScript: скобки, кавычки.
    Полный парсинг через eval/Function небезопасен, используем эвристики.
    """
    errors: List[CodeError] = []
    lines = code.split('\n')
    
    # Проверка парности скобок
    opens = {'(': 0, '[': 0, '{': 0}
    closes = {')': '(', ']': '[', '}': '{'}
    stack: List[tuple] = []  # (char, line, col)
    
    in_string = None
    in_regex = False
    escape = False
    i = 0
    total = len(code)
    
    while i < total:
        ch = code[i]
        line_num = code[:i].count('\n') + 1
        col = i - code.rfind('\n', 0, i) - 1 if '\n' in code[:i] else i
        
        if escape:
            escape = False
            i += 1
            continue
        
        if ch == '\\' and (in_string or in_regex):
            escape = True
            i += 1
            continue
        
        if in_string:
            if ch == in_string:
                in_string = None
            i += 1
            continue
        
        if ch in ('"', "'", '`') and not in_string:
            in_string = ch
            i += 1
            continue
        
        if ch in '([{':
            stack.append((ch, line_num, col))
            i += 1
            continue
        
        if ch in ')]}':
            if not stack:
                errors.append(CodeError(
                    line=line_num, column=col,
                    message=f"Лишняя закрывающая скобка {ch}",
                    code="extra-bracket",
                    hint=f"Удалите лишнюю {ch} или добавьте открывающую скобку"
                ))
            elif stack[-1][0] != closes[ch]:
                expected = closes[ch]
                errors.append(CodeError(
                    line=line_num, column=col,
                    message=f"Несоответствие скобок: получено {ch}, ожидалось {expected}",
                    code="mismatched-bracket",
                    hint="Проверьте парность скобок () [] {}"
                ))
            else:
                stack.pop()
            i += 1
            continue
        
        i += 1
    
    if in_string:
        errors.append(CodeError(
            line=code.count('\n') + 1, column=0,
            message="Не закрыта кавычка в строке",
            code="unclosed-quote",
            hint="Добавьте закрывающую кавычку"
        ))
    
    for char, ln, col in reversed(stack):
        pair = {'(': ')', '[': ']', '{': '}'}[char]
        errors.append(CodeError(
            line=ln, column=col,
            message=f"Не закрыта скобка {char}",
            code="unclosed-bracket",
            hint=f"Добавьте закрывающую скобку {pair}"
        ))
    
    return errors


def validate_all(html: str, css: str, js: str) -> dict:
    """
    Проверка всего кода. Возвращает словарь с ошибками по типам.
    """
    return {
        'html': validate_html(html),
        'css': validate_css(css),
        'js': validate_javascript(js)
    }
