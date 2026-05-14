"""Создание полного курса с 25 темами."""
from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Assignment, Quiz, Question, Answer, StandaloneAssignment


class Command(BaseCommand):
    help = 'Создаёт полный курс с 25 темами по веб-программированию'

    def handle(self, *args, **options):
        # Создаём курсы
        html_basics, _ = Course.objects.get_or_create(
            slug='html-basics',
            defaults={
                'title': 'Основы HTML',
                'short_description': 'Изучи основы языка разметки HTML. Научись создавать структуру веб-страниц, работать с текстом, списками, ссылками и изображениями.',
                'description': '''Курс "Основы HTML" познакомит вас с фундаментальными понятиями веб-разработки. Вы научитесь создавать структуру веб-страниц, использовать основные HTML-теги, работать с текстом, списками, ссылками и изображениями. Курс подходит для начинающих и не требует предварительных знаний.''',
                'order': 1,
                'icon': '📝',
            }
        )

        html_advanced, _ = Course.objects.get_or_create(
            slug='html-advanced',
            defaults={
                'title': 'Продвинутый HTML',
                'short_description': 'Углубленное изучение HTML: семантические элементы, формы, таблицы, мультимедиа и современные возможности HTML5.',
                'description': '''Курс "Продвинутый HTML" поможет вам освоить современные возможности HTML5. Вы изучите семантические элементы, научитесь создавать формы, таблицы, встраивать мультимедиа контент и использовать новые API.''',
                'order': 2,
                'icon': '🚀',
            }
        )

        css_course, _ = Course.objects.get_or_create(
            slug='css-course',
            defaults={
                'title': 'Изучение CSS',
                'short_description': 'Освой каскадные таблицы стилей. Научись создавать красивые и современные веб-страницы с адаптивным дизайном.',
                'description': '''Курс "Изучение CSS" научит вас оформлять веб-страницы. Вы изучите селекторы, свойства, позиционирование, flexbox, grid и основы адаптивной верстки. Создавайте красивые и современные интерфейсы!''',
                'order': 3,
                'icon': '🎨',
            }
        )

        js_course, _ = Course.objects.get_or_create(
            slug='javascript-course',
            defaults={
                'title': 'Изучение JavaScript',
                'short_description': 'Изучи JavaScript и добавь интерактивность своим веб-страницам. Переменные, функции, DOM, события и многое другое.',
                'description': '''Курс "Изучение JavaScript" познакомит вас с программированием на JavaScript. Вы изучите основы языка, работу с DOM, обработку событий, валидацию форм и создание интерактивных веб-приложений.''',
                'order': 4,
                'icon': '⚙️',
            }
        )

        # Темы курса
        lessons_data = [
            # Основы HTML (1-6)
            (html_basics, 1, 'vvedenie-v-veb-razrabotku', 'Введение в веб-разработку', 
             '''<h2>Что такое веб-разработка?</h2>
             <p>Веб-разработка — это процесс создания веб-сайтов и веб-приложений. Она включает в себя:</p>
             <ul>
                 <li><strong>Frontend</strong> — видимая часть сайта (HTML, CSS, JavaScript)</li>
                 <li><strong>Backend</strong> — серверная часть (базы данных, серверы)</li>
             </ul>
             <h3>Основные технологии:</h3>
             <table class="table table-bordered">
                 <thead>
                     <tr>
                         <th>Технология</th>
                         <th>Назначение</th>
                     </tr>
                 </thead>
                 <tbody>
                     <tr>
                         <td>HTML</td>
                         <td>Структура страницы</td>
                     </tr>
                     <tr>
                         <td>CSS</td>
                         <td>Оформление и стили</td>
                     </tr>
                     <tr>
                         <td>JavaScript</td>
                         <td>Интерактивность</td>
                     </tr>
                 </tbody>
             </table>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Мой первый сайт</title>\n</head>\n<body>\n  <h1>Привет, мир!</h1>\n</body>\n</html>',
             '', ''),
            
            (html_basics, 2, 'struktura-html-dokumenta', 'Структура HTML-документа',
             '''<h2>Базовая структура HTML</h2>
             <p>Каждый HTML-документ имеет определенную структуру:</p>
             <pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="ru"&gt;
  &lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Заголовок страницы&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    Содержимое страницы
  &lt;/body&gt;
&lt;/html&gt;</code></pre>
             <h3>Элементы структуры:</h3>
             <ul>
                 <li><code>&lt;!DOCTYPE html&gt;</code> — объявление типа документа</li>
                 <li><code>&lt;html&gt;</code> — корневой элемент</li>
                 <li><code>&lt;head&gt;</code> — метаданные (не видны на странице)</li>
                 <li><code>&lt;body&gt;</code> — видимое содержимое</li>
             </ul>''',
             '<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="UTF-8">\n  <title>Моя страница</title>\n</head>\n<body>\n  <h1>Заголовок</h1>\n  <p>Параграф текста</p>\n</body>\n</html>',
             '', ''),
            
            (html_basics, 3, 'osnovnye-tegi-i-atributy', 'Основные теги и атрибуты',
             '''<h2>Основные HTML-теги</h2>
             <p>Теги — это элементы разметки, которые определяют структуру и содержание страницы.</p>
             <h3>Текстовые теги:</h3>
             <ul>
                 <li><code>&lt;h1&gt;</code> - <code>&lt;h6&gt;</code> — заголовки разных уровней</li>
                 <li><code>&lt;p&gt;</code> — параграф</li>
                 <li><code>&lt;strong&gt;</code> — жирный текст</li>
                 <li><code>&lt;em&gt;</code> — курсив</li>
             </ul>
             <h3>Атрибуты:</h3>
             <p>Атрибуты добавляют дополнительную информацию к тегам:</p>
             <pre><code>&lt;div class="container" id="main"&gt;
  Содержимое
&lt;/div&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Теги и атрибуты</title>\n</head>\n<body>\n  <h1 class="title">Главный заголовок</h1>\n  <p id="intro">Введение в тему</p>\n  <div class="content">\n    <p>Основной <strong>важный</strong> текст</p>\n  </div>\n</body>\n</html>',
             '', ''),
            
            (html_basics, 4, 'rabota-s-tekstom', 'Работа с текстом в HTML',
             '''<h2>Форматирование текста</h2>
             <p>HTML предоставляет множество способов форматирования текста:</p>
             <table class="table">
                 <tr>
                     <th>Тег</th>
                     <th>Назначение</th>
                 </tr>
                 <tr>
                     <td><code>&lt;strong&gt;</code></td>
                     <td>Важный текст (жирный)</td>
                 </tr>
                 <tr>
                     <td><code>&lt;em&gt;</code></td>
                     <td>Выделенный текст (курсив)</td>
                 </tr>
                 <tr>
                     <td><code>&lt;mark&gt;</code></td>
                     <td>Выделение маркером</td>
                 </tr>
                 <tr>
                     <td><code>&lt;code&gt;</code></td>
                     <td>Код</td>
                 </tr>
             </table>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Текст</title>\n</head>\n<body>\n  <h1>Форматирование текста</h1>\n  <p>Это <strong>важный</strong> текст.</p>\n  <p>Это <em>выделенный</em> текст.</p>\n  <p>Это <mark>выделенный</mark> текст.</p>\n  <p>Код: <code>console.log()</code></p>\n</body>\n</html>',
             '', ''),
            
            (html_basics, 5, 'spiski-v-html', 'Списки в HTML',
             '''<h2>Создание списков</h2>
             <p>В HTML есть два основных типа списков:</p>
             <h3>Маркированный список (ul):</h3>
             <pre><code>&lt;ul&gt;
  &lt;li&gt;Элемент 1&lt;/li&gt;
  &lt;li&gt;Элемент 2&lt;/li&gt;
&lt;/ul&gt;</code></pre>
             <h3>Нумерованный список (ol):</h3>
             <pre><code>&lt;ol&gt;
  &lt;li&gt;Первый пункт&lt;/li&gt;
  &lt;li&gt;Второй пункт&lt;/li&gt;
&lt;/ol&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Списки</title>\n</head>\n<body>\n  <h2>Маркированный список</h2>\n  <ul>\n    <li>Яблоко</li>\n    <li>Банан</li>\n    <li>Апельсин</li>\n  </ul>\n  <h2>Нумерованный список</h2>\n  <ol>\n    <li>Первый</li>\n    <li>Второй</li>\n    <li>Третий</li>\n  </ol>\n</body>\n</html>',
             '', ''),
            
            (html_basics, 6, 'giperssylki', 'Гиперссылки',
             '''<h2>Создание ссылок</h2>
             <p>Ссылки создаются с помощью тега <code>&lt;a&gt;</code>:</p>
             <pre><code>&lt;a href="https://example.com"&gt;Текст ссылки&lt;/a&gt;</code></pre>
             <h3>Типы ссылок:</h3>
             <ul>
                 <li><strong>Внешние</strong> — на другие сайты</li>
                 <li><strong>Внутренние</strong> — на страницы того же сайта</li>
                 <li><strong>Якоря</strong> — на элементы страницы</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Ссылки</title>\n</head>\n<body>\n  <h1>Гиперссылки</h1>\n  <p>Внешняя ссылка: <a href="https://example.com">Пример</a></p>\n  <p>Внутренняя ссылка: <a href="#section">К разделу</a></p>\n  <p>Email: <a href="mailto:test@example.com">Написать</a></p>\n</body>\n</html>',
             '', ''),
            
            # Продвинутый HTML (7-12)
            (html_advanced, 7, 'izobrazheniya', 'Изображения',
             '''<h2>Работа с изображениями</h2>
             <p>Изображения добавляются тегом <code>&lt;img&gt;</code>:</p>
             <pre><code>&lt;img src="путь/к/изображению.jpg" alt="Описание"&gt;</code></pre>
             <h3>Важные атрибуты:</h3>
             <ul>
                 <li><code>src</code> — путь к изображению</li>
                 <li><code>alt</code> — альтернативный текст (обязателен!)</li>
                 <li><code>width</code> и <code>height</code> — размеры</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Изображения</title>\n</head>\n<body>\n  <h1>Работа с изображениями</h1>\n  <img src="https://via.placeholder.com/300" alt="Пример изображения" width="300">\n</body>\n</html>',
             '', ''),
            
            (html_advanced, 8, 'tablitsy', 'Таблицы',
             '''<h2>Создание таблиц</h2>
             <p>Таблицы создаются с помощью тегов <code>&lt;table&gt;</code>, <code>&lt;tr&gt;</code>, <code>&lt;td&gt;</code>:</p>
             <pre><code>&lt;table&gt;
  &lt;tr&gt;
    &lt;th&gt;Заголовок 1&lt;/th&gt;
    &lt;th&gt;Заголовок 2&lt;/th&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Ячейка 1&lt;/td&gt;
    &lt;td&gt;Ячейка 2&lt;/td&gt;
  &lt;/tr&gt;
&lt;/table&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Таблицы</title>\n</head>\n<body>\n  <table border="1">\n    <tr>\n      <th>Имя</th>\n      <th>Возраст</th>\n    </tr>\n    <tr>\n      <td>Иван</td>\n      <td>25</td>\n    </tr>\n    <tr>\n      <td>Мария</td>\n      <td>30</td>\n    </tr>\n  </table>\n</body>\n</html>',
             '', ''),
            
            (html_advanced, 9, 'formy', 'Формы',
             '''<h2>Создание форм</h2>
             <p>Формы создаются тегом <code>&lt;form&gt;</code>:</p>
             <pre><code>&lt;form action="/submit" method="post"&gt;
  &lt;input type="text" name="username" placeholder="Имя"&gt;
  &lt;input type="email" name="email" placeholder="Email"&gt;
  &lt;button type="submit"&gt;Отправить&lt;/button&gt;
&lt;/form&gt;</code></pre>
             <h3>Типы полей:</h3>
             <ul>
                 <li><code>text</code> — текстовое поле</li>
                 <li><code>email</code> — email</li>
                 <li><code>password</code> — пароль</li>
                 <li><code>checkbox</code> — чекбокс</li>
                 <li><code>radio</code> — радиокнопка</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Формы</title>\n</head>\n<body>\n  <form>\n    <label>Имя:</label>\n    <input type="text" name="name" placeholder="Введите имя">\n    <br><br>\n    <label>Email:</label>\n    <input type="email" name="email" placeholder="email@example.com">\n    <br><br>\n    <button type="submit">Отправить</button>\n  </form>\n</body>\n</html>',
             '', ''),
            
            (html_advanced, 10, 'semanticheskie-elementy', 'Семантические элементы HTML5',
             '''<h2>Семантические элементы</h2>
             <p>HTML5 ввел семантические элементы для лучшей структуры:</p>
             <ul>
                 <li><code>&lt;header&gt;</code> — шапка</li>
                 <li><code>&lt;nav&gt;</code> — навигация</li>
                 <li><code>&lt;main&gt;</code> — основное содержимое</li>
                 <li><code>&lt;article&gt;</code> — статья</li>
                 <li><code>&lt;section&gt;</code> — раздел</li>
                 <li><code>&lt;footer&gt;</code> — подвал</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Семантика</title>\n</head>\n<body>\n  <header>\n    <h1>Заголовок сайта</h1>\n  </header>\n  <nav>\n    <a href="#">Главная</a>\n    <a href="#">О нас</a>\n  </nav>\n  <main>\n    <article>\n      <h2>Статья</h2>\n      <p>Содержимое статьи</p>\n    </article>\n  </main>\n  <footer>\n    <p>Подвал сайта</p>\n  </footer>\n</body>\n</html>',
             '', ''),
            
            (html_advanced, 11, 'multimedia', 'Встраивание мультимедиа',
             '''<h2>Видео и аудио</h2>
             <h3>Видео:</h3>
             <pre><code>&lt;video controls&gt;
  &lt;source src="video.mp4" type="video/mp4"&gt;
&lt;/video&gt;</code></pre>
             <h3>Аудио:</h3>
             <pre><code>&lt;audio controls&gt;
  &lt;source src="audio.mp3" type="audio/mpeg"&gt;
&lt;/audio&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Мультимедиа</title>\n</head>\n<body>\n  <h1>Видео</h1>\n  <video controls width="400">\n    <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">\n    Ваш браузер не поддерживает видео.\n  </video>\n</body>\n</html>',
             '', ''),
            
            (html_advanced, 12, 'klassy-i-identifikatory', 'Классы и идентификаторы',
             '''<h2>Классы и ID</h2>
             <p><code>class</code> — для группировки элементов (может быть несколько)</p>
             <p><code>id</code> — уникальный идентификатор (только один на странице)</p>
             <pre><code>&lt;div class="container" id="main"&gt;
  Содержимое
&lt;/div&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Классы и ID</title>\n</head>\n<body>\n  <div id="header" class="container">\n    <h1>Заголовок</h1>\n  </div>\n  <div class="container content">\n    <p>Основной контент</p>\n  </div>\n</body>\n</html>',
             '', ''),
            
            # CSS (13-14)
            (css_course, 13, 'podklyuchenie-css', 'Подключение CSS к HTML',
             '''<h2>Способы подключения CSS</h2>
             <h3>1. Внешний файл (рекомендуется):</h3>
             <pre><code>&lt;link rel="stylesheet" href="styles.css"&gt;</code></pre>
             <h3>2. Внутри &lt;head&gt;:</h3>
             <pre><code>&lt;style&gt;
  body { color: blue; }
&lt;/style&gt;</code></pre>
             <h3>3. Инлайн стили:</h3>
             <pre><code>&lt;p style="color: red;"&gt;Текст&lt;/p&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>CSS</title>\n  <style>\n    body {\n      font-family: Arial;\n      color: #333;\n    }\n    h1 {\n      color: #6366f1;\n    }\n  </style>\n</head>\n<body>\n  <h1>Заголовок</h1>\n  <p>Текст с примененными стилями</p>\n</body>\n</html>',
             'body {\n  font-family: Arial, sans-serif;\n  color: #333;\n  padding: 20px;\n}\n\nh1 {\n  color: #6366f1;\n  font-size: 2em;\n}', ''),
            
            (css_course, 14, 'adaptivnaya-verstka', 'Основы адаптивной верстки',
             '''<h2>Адаптивный дизайн</h2>
             <p>Медиа-запросы позволяют применять стили в зависимости от размера экрана:</p>
             <pre><code>@media (max-width: 768px) {
  .container {
    width: 100%;
  }
}</code></pre>
             <h3>Viewport:</h3>
             <pre><code>&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>Адаптивность</title>\n</head>\n<body>\n  <div class="container">\n    <h1>Адаптивный дизайн</h1>\n    <p>Этот контент адаптируется под размер экрана</p>\n  </div>\n</body>\n</html>',
             '.container {\n  max-width: 1200px;\n  margin: 0 auto;\n  padding: 20px;\n}\n\n@media (max-width: 768px) {\n  .container {\n    padding: 10px;\n  }\n}', ''),
            
            # JavaScript (15-24)
            (js_course, 15, 'vvedenie-v-javascript', 'Введение в JavaScript',
             '''<h2>Что такое JavaScript?</h2>
             <p>JavaScript — язык программирования для создания интерактивных веб-страниц.</p>
             <h3>Возможности:</h3>
             <ul>
                 <li>Динамическое изменение содержимого</li>
                 <li>Обработка событий</li>
                 <li>Работа с формами</li>
                 <li>Взаимодействие с сервером</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>JavaScript</title>\n</head>\n<body>\n  <h1>Привет, JavaScript!</h1>\n  <p id="demo"></p>\n</body>\n</html>',
             '', 'document.getElementById("demo").innerHTML = "JavaScript работает!";'),
            
            (js_course, 16, 'podklyuchenie-javascript', 'Подключение JavaScript к HTML',
             '''<h2>Способы подключения</h2>
             <h3>1. Внешний файл:</h3>
             <pre><code>&lt;script src="script.js"&gt;&lt;/script&gt;</code></pre>
             <h3>2. Внутри страницы:</h3>
             <pre><code>&lt;script&gt;
  console.log("Привет!");
&lt;/script&gt;</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>JS подключение</title>\n</head>\n<body>\n  <h1>JavaScript</h1>\n</body>\n<script>\n  alert("JavaScript подключен!");\n</script>\n</html>',
             '', 'console.log("Скрипт загружен!");'),
            
            (js_course, 17, 'peremennye-i-tipy', 'Переменные и типы данных',
             '''<h2>Переменные</h2>
             <p>Объявление переменных:</p>
             <pre><code>let name = "Иван";
const age = 25;
var city = "Москва";</code></pre>
             <h3>Типы данных:</h3>
             <ul>
                 <li><code>String</code> — строка</li>
                 <li><code>Number</code> — число</li>
                 <li><code>Boolean</code> — true/false</li>
                 <li><code>Array</code> — массив</li>
                 <li><code>Object</code> — объект</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Переменные</title>\n</head>\n<body>\n  <h1>Переменные</h1>\n  <p id="output"></p>\n</body>\n</html>',
             '', 'let name = "Иван";\nlet age = 25;\ndocument.getElementById("output").innerHTML = `Имя: ${name}, Возраст: ${age}`;'),
            
            (js_course, 18, 'operatory', 'Операторы и выражения',
             '''<h2>Операторы</h2>
             <h3>Арифметические:</h3>
             <pre><code>let sum = 5 + 3;
let diff = 10 - 2;
let mult = 4 * 2;
let div = 8 / 2;</code></pre>
             <h3>Логические:</h3>
             <pre><code>let result = (5 > 3) && (2 < 4);</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Операторы</title>\n</head>\n<body>\n  <h1>Операторы</h1>\n  <p id="result"></p>\n</body>\n</html>',
             '', 'let a = 10;\nlet b = 5;\nlet sum = a + b;\nlet mult = a * b;\ndocument.getElementById("result").innerHTML = `Сумма: ${sum}, Произведение: ${mult}`;'),
            
            (js_course, 19, 'uslovnye-konstruktsii', 'Условные конструкции',
             '''<h2>Условия</h2>
             <pre><code>if (age >= 18) {
  console.log("Совершеннолетний");
} else {
  console.log("Несовершеннолетний");
}</code></pre>
             <h3>Switch:</h3>
             <pre><code>switch(day) {
  case 1: console.log("Понедельник"); break;
  default: console.log("Другой день");
}</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Условия</title>\n</head>\n<body>\n  <h1>Условные конструкции</h1>\n  <p id="output"></p>\n</body>\n</html>',
             '', 'let age = 20;\nlet message;\nif (age >= 18) {\n  message = "Совершеннолетний";\n} else {\n  message = "Несовершеннолетний";\n}\ndocument.getElementById("output").innerHTML = message;'),
            
            (js_course, 20, 'tsikly', 'Циклы',
             '''<h2>Циклы в JavaScript</h2>
             <h3>For:</h3>
             <pre><code>for (let i = 0; i < 5; i++) {
  console.log(i);
}</code></pre>
             <h3>While:</h3>
             <pre><code>let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Циклы</title>\n</head>\n<body>\n  <h1>Циклы</h1>\n  <ul id="list"></ul>\n</body>\n</html>',
             '', 'let list = document.getElementById("list");\nfor (let i = 1; i <= 5; i++) {\n  let li = document.createElement("li");\n  li.textContent = `Элемент ${i}`;\n  list.appendChild(li);\n}'),
            
            (js_course, 21, 'funktsii', 'Функции',
             '''<h2>Функции</h2>
             <h3>Объявление функции:</h3>
             <pre><code>function greet(name) {
  return "Привет, " + name;
}</code></pre>
             <h3>Стрелочная функция:</h3>
             <pre><code>const greet = (name) => {
  return "Привет, " + name;
}</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Функции</title>\n</head>\n<body>\n  <h1>Функции</h1>\n  <p id="output"></p>\n</body>\n</html>',
             '', 'function greet(name) {\n  return `Привет, ${name}!`;\n}\n\ndocument.getElementById("output").innerHTML = greet("Иван");'),
            
            (js_course, 22, 'rabota-s-dom', 'Работа с DOM',
             '''<h2>DOM (Document Object Model)</h2>
             <p>DOM — представление HTML-документа в виде дерева объектов.</p>
             <h3>Основные методы:</h3>
             <ul>
                 <li><code>getElementById()</code> — найти по ID</li>
                 <li><code>querySelector()</code> — найти по селектору</li>
                 <li><code>createElement()</code> — создать элемент</li>
                 <li><code>appendChild()</code> — добавить элемент</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>DOM</title>\n</head>\n<body>\n  <h1>Работа с DOM</h1>\n  <div id="container"></div>\n  <button onclick="addElement()">Добавить элемент</button>\n</body>\n</html>',
             '', 'function addElement() {\n  let container = document.getElementById("container");\n  let p = document.createElement("p");\n  p.textContent = "Новый элемент!";\n  container.appendChild(p);\n}'),
            
            (js_course, 23, 'obrabotka-sobytij', 'Обработка событий',
             '''<h2>События</h2>
             <p>События — действия пользователя (клик, наведение, ввод текста).</p>
             <h3>Способы обработки:</h3>
             <pre><code>// HTML атрибут
&lt;button onclick="handleClick()"&gt;Кнопка&lt;/button&gt;

// JavaScript
button.addEventListener("click", handleClick);</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>События</title>\n</head>\n<body>\n  <h1>Обработка событий</h1>\n  <button id="btn">Нажми меня</button>\n  <p id="message"></p>\n</body>\n</html>',
             '', 'document.getElementById("btn").addEventListener("click", function() {\n  document.getElementById("message").innerHTML = "Кнопка нажата!";\n});'),
            
            (js_course, 24, 'validatsiya-form', 'Валидация форм с помощью JavaScript',
             '''<h2>Валидация форм</h2>
             <p>Проверка данных формы перед отправкой:</p>
             <pre><code>function validateForm() {
  let name = document.getElementById("name").value;
  if (name === "") {
    alert("Введите имя!");
    return false;
  }
  return true;
}</code></pre>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <title>Валидация</title>\n</head>\n<body>\n  <form id="myForm" onsubmit="return validateForm()">\n    <input type="text" id="name" placeholder="Имя" required>\n    <input type="email" id="email" placeholder="Email" required>\n    <button type="submit">Отправить</button>\n  </form>\n  <p id="error"></p>\n</body>\n</html>',
             '', 'function validateForm() {\n  let name = document.getElementById("name").value;\n  let email = document.getElementById("email").value;\n  \n  if (name === "") {\n    document.getElementById("error").innerHTML = "Введите имя!";\n    return false;\n  }\n  \n  if (!email.includes("@")) {\n    document.getElementById("error").innerHTML = "Неверный email!";\n    return false;\n  }\n  \n  return true;\n}'),
            
            # Итоговый проект (25)
            (js_course, 25, 'itogovyj-proekt', 'Итоговый проект (интерактивный сайт)',
             '''<h2>Итоговый проект</h2>
             <p>Создай интерактивный сайт, используя все изученные технологии:</p>
             <ul>
                 <li>HTML — структура</li>
                 <li>CSS — стили и адаптивность</li>
                 <li>JavaScript — интерактивность</li>
             </ul>
             <h3>Требования:</h3>
             <ul>
                 <li>Несколько страниц или разделов</li>
                 <li>Адаптивный дизайн</li>
                 <li>Интерактивные элементы</li>
                 <li>Валидация форм</li>
             </ul>''',
             '<!DOCTYPE html>\n<html>\n<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>Мой проект</title>\n</head>\n<body>\n  <header>\n    <h1>Мой интерактивный сайт</h1>\n  </header>\n  <main>\n    <p>Начни создавать свой проект здесь!</p>\n  </main>\n</body>\n</html>',
             'body {\n  font-family: Arial, sans-serif;\n  max-width: 1200px;\n  margin: 0 auto;\n  padding: 20px;\n}\n\nheader {\n  background: #6366f1;\n  color: white;\n  padding: 20px;\n  border-radius: 8px;\n}', '// Добавь интерактивность\nconsole.log("Проект запущен!");'),
        ]

        # Создаём уроки
        for course, order, slug, title, content, html, css, js in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                course=course,
                slug=slug,
                defaults={
                    'title': title,
                    'content': content,
                    'example_code_html': html,
                    'example_code_css': css,
                    'example_code_js': js,
                    'order': order,
                }
            )
            if created:
                self.stdout.write(f'Создан урок: {title}')

            # Создаём задание для каждого урока
            Assignment.objects.get_or_create(
                lesson=lesson,
                title=f'Задание: {title}',
                defaults={
                    'description': f'Выполни практическое задание по теме "{title}". Примени изученный материал на практике.',
                    'order': 1,
                }
            )

        # Создаём дополнительные задания
        standalone_assignments = [
            ('Создать личную страницу', 'Создай свою личную страницу с информацией о себе, используя HTML и CSS.', 'easy'),
            ('Интерактивная форма', 'Создай форму обратной связи с валидацией на JavaScript.', 'medium'),
            ('Галерея изображений', 'Создай галерею изображений с возможностью просмотра в полном размере.', 'medium'),
            ('Калькулятор', 'Создай простой калькулятор на JavaScript.', 'hard'),
            ('Игра "Угадай число"', 'Создай игру, где пользователь угадывает загаданное число.', 'medium'),
        ]

        for title, description, difficulty in standalone_assignments:
            StandaloneAssignment.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'difficulty': difficulty,
                }
            )

        self.stdout.write(self.style.SUCCESS('✅ Создано 25 уроков и дополнительные задания!'))
        self.stdout.write(self.style.SUCCESS('Теперь можно зайти в админ-панель и добавить тесты к урокам.'))
