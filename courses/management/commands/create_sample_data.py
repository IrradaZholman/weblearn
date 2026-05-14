"""Создание примерных курсов и уроков для демонстрации."""
from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Assignment


class Command(BaseCommand):
    help = 'Создаёт примерный курс HTML для демонстрации'

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            slug='html',
            defaults={
                'title': 'Основы HTML',
                'description': 'Изучи основы разметки веб-страниц. Узнай про теги, атрибуты и структуру документа.',
                'order': 1,
            }
        )
        if created:
            self.stdout.write('Создан курс: Основы HTML')

        lesson1, _ = Lesson.objects.update_or_create(
            course=course,
            slug='vvedenie',
            defaults={
                'title': 'Введение в HTML',
                'order': 1,
                'content': '''
<p class="lesson-lead">HTML (HyperText Markup Language) — это язык разметки для создания веб-страниц. С его помощью задают заголовки, абзацы, ссылки, списки и другие элементы страницы.</p>

<h2>Основные понятия</h2>
<ul>
<li><strong>Тег</strong> — элемент разметки, например <code>&lt;h1&gt;</code>, <code>&lt;p&gt;</code>, <code>&lt;div&gt;</code></li>
<li><strong>Атрибут</strong> — дополнительная информация о теге, например <code>class="title"</code></li>
<li><strong>Элемент</strong> — открывающий тег, содержимое и закрывающий тег (если тег парный)</li>
</ul>

<h2>Структура документа</h2>
<ul>
<li><code>&lt;!DOCTYPE html&gt;</code> — объявление типа документа (HTML5)</li>
<li><code>&lt;html&gt;</code> — корневой элемент страницы</li>
<li><code>&lt;head&gt;</code> — служебная информация (заголовок вкладки, метаданные, стили)</li>
<li><code>&lt;body&gt;</code> — всё, что видит пользователь на странице</li>
</ul>

<p class="lesson-cta">Попробуй создать свою первую страницу в <a href="/editor/">редакторе WebLearn</a>!</p>
'''.strip(),
            }
        )

        Assignment.objects.get_or_create(
            lesson=lesson1,
            title='Моя первая страница',
            defaults={
                'description': 'Создай страницу с заголовком <h1> и двумя параграфами <p>. Добавь свои стили в CSS.',
                'order': 1,
            }
        )

        lesson2, _ = Lesson.objects.update_or_create(
            course=course,
            slug='ssylki-i-izobrazheniya',
            defaults={
                'title': 'Ссылки и изображения',
                'order': 2,
                'content': '''
<p class="lesson-lead">Ссылки и картинки — то, из чего часто состоят учебные страницы. Разберём синтаксис и обязательные атрибуты.</p>

<h2>Ссылки</h2>
<p>Создаются тегом <code>&lt;a&gt;</code> с атрибутом <code>href</code>:</p>
<pre><code>&lt;a href="https://example.com"&gt;Текст ссылки&lt;/a&gt;</code></pre>

<h2>Изображения</h2>
<p>Тег <code>&lt;img&gt;</code> — одиночный (закрывающий тег не нужен):</p>
<pre><code>&lt;img src="путь-к-картинке.jpg" alt="Краткое описание"&gt;</code></pre>
<p>Атрибут <code>alt</code> обязателен для доступности: при ошибке загрузки или для скринридеров показывается этот текст.</p>
'''.strip(),
            }
        )

        Assignment.objects.get_or_create(
            lesson=lesson2,
            title='Страница со ссылками',
            defaults={
                'description': 'Создай страницу с несколькими ссылками на разные сайты. Оформи их с помощью CSS.',
                'order': 1,
            }
        )

        self.stdout.write(self.style.SUCCESS('Готово! Зайди в Курсы и начни обучение.'))
