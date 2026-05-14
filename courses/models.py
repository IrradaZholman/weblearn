from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Course(models.Model):
    """Курс (модуль) обучения."""
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    short_description = models.TextField('Краткое описание', max_length=500, blank=True, help_text='Для главной страницы курса')
    video_url = models.URLField('URL вводного видео', blank=True, help_text='YouTube или другой видеохостинг')
    image = models.ImageField('Изображение курса', upload_to='courses/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    icon = models.CharField('Иконка', max_length=50, default='book', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'course_slug': self.slug})


class Lesson(models.Model):
    """Урок в рамках курса."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL')
    content = models.TextField(
        'Содержание',
        help_text='HTML-разметка: заголовки h2/h3, p, ul/ol, pre/code. Угловые скобки в тексте задавайте как &lt; &gt; или оборачивайте в code.',
    )
    example_code_html = models.TextField('Пример HTML кода', blank=True, help_text='Код для встроенного эмулятора')
    example_code_css = models.TextField('Пример CSS кода', blank=True)
    example_code_js = models.TextField('Пример JavaScript кода', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'slug']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Assignment(models.Model):
    """Задание к уроку."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'{self.lesson.title} — {self.title}'


class Submission(models.Model):
    """Работа ученика (на ручную проверку)."""
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('accepted', 'Принято'),
        ('revision', 'Нужно доработать'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    standalone_assignment = models.ForeignKey('StandaloneAssignment', on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='submissions')
    code = models.TextField('Код', blank=True)
    comment = models.TextField('Комментарий ученика', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    grade = models.PositiveIntegerField('Оценка', null=True, blank=True, help_text='Оценка от 1 до 5')
    reviewer_comment = models.TextField('Комментарий проверяющего', blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        assignment_name = self.assignment.title if self.assignment else (self.standalone_assignment.title if self.standalone_assignment else 'Неизвестно')
        return f'{assignment_name} — {self.user or "Гость"} ({self.get_status_display()})'


class StandaloneAssignment(models.Model):
    """Дополнительное задание, не привязанное к конкретному уроку."""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    difficulty = models.CharField('Сложность', max_length=20, choices=[
        ('easy', 'Легкое'),
        ('medium', 'Среднее'),
        ('hard', 'Сложное'),
    ], default='medium')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Дополнительное задание'
        verbose_name_plural = 'Дополнительные задания'

    def __str__(self):
        return self.title


class Quiz(models.Model):
    """Тест для проверки знаний."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True, help_text='Если не указан урок, это общий тест по курсу')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True, help_text='Для общего теста по курсу')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    passing_score = models.PositiveIntegerField('Проходной балл (%)', default=70)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопрос в тесте."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Текст вопроса')
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.quiz.title} — {self.text[:50]}'


class Answer(models.Model):
    """Вариант ответа на вопрос."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Текст ответа', max_length=500)
    is_correct = models.BooleanField('Правильный ответ', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.question.text[:30]} — {self.text[:30]}'


class QuizAttempt(models.Model):
    """Попытка прохождения теста пользователем."""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.PositiveIntegerField('Балл (%)', default=0)
    passed = models.BooleanField('Пройден', default=False)
    answers = models.JSONField('Ответы пользователя', default=dict, help_text='{question_id: answer_id}')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Попытка прохождения теста'
        verbose_name_plural = 'Попытки прохождения тестов'
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user.username} — {self.quiz.title} ({self.score}%)'


class UserProgress(models.Model):
    """Прогресс пользователя по урокам и курсам."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress', null=True, blank=True)
    completed = models.BooleanField('Завершено', default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'lesson'], ['user', 'course']]
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'

    def __str__(self):
        if self.lesson:
            return f'{self.user.username} — {self.lesson.title}'
        return f'{self.user.username} — {self.course.title}'


class CourseReview(models.Model):
    """Отзыв о курсе."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.PositiveIntegerField('Оценка', choices=[(i, i) for i in range(1, 6)], default=5)
    text = models.TextField('Текст отзыва', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.course.title} ({self.rating}★)'
