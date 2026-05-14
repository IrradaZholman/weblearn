import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from courses.models import Assignment, Submission, StandaloneAssignment
from .code_validator import validate_all, CodeError
from .chatbot import get_chat_response


def editor(request, assignment_id=None):
    assignment = get_object_or_404(Assignment, pk=assignment_id) if assignment_id else None
    return render(request, 'editor/editor.html', {'assignment': assignment})


def editor_standalone(request, standalone_assignment_id=None):
    """Редактор без привязки к заданию — для экспериментов или дополнительных заданий."""
    standalone_assignment = None
    if standalone_assignment_id:
        standalone_assignment = get_object_or_404(StandaloneAssignment, pk=standalone_assignment_id)
    return render(request, 'editor/editor.html', {
        'assignment': None,
        'standalone_assignment': standalone_assignment
    })


def builder(request):
    """Визуальный конструктор страниц для начинающих."""
    return render(request, 'editor/builder.html')


def submit_work(request):
    if request.method != 'POST':
        return redirect('editor:standalone')

    assignment_id = request.POST.get('assignment_id')
    standalone_assignment_id = request.POST.get('standalone_assignment_id')
    code = request.POST.get('code', '')
    comment = request.POST.get('comment', '')

    if not assignment_id and not standalone_assignment_id:
        messages.warning(request, 'Выберите задание для отправки.')
        return redirect('editor:standalone')

    user = request.user if request.user.is_authenticated else None

    if assignment_id:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        Submission.objects.create(
            assignment=assignment,
            user=user,
            code=code,
            comment=comment,
        )
        messages.success(request, 'Работа отправлена на проверку!')
        return redirect('courses:lesson_detail', 
                       course_slug=assignment.lesson.course.slug, 
                       lesson_slug=assignment.lesson.slug)
    else:
        standalone_assignment = get_object_or_404(StandaloneAssignment, pk=standalone_assignment_id)
        Submission.objects.create(
            standalone_assignment=standalone_assignment,
            user=user,
            code=code,
            comment=comment,
        )
        messages.success(request, 'Работа отправлена на проверку!')
        return redirect('courses:standalone_assignments')


def _errors_to_dict(errors_list):
    """Преобразует список CodeError в JSON-сериализуемый формат."""
    return [
        {
            'line': e.line,
            'column': e.column,
            'end_line': e.end_line,
            'end_column': e.end_column,
            'message': e.message,
            'code': e.code,
            'severity': e.severity,
            'hint': e.hint,
        }
        for e in errors_list
    ]


@require_POST
def api_validate(request):
    """API: проверка кода. POST {html, css, js} -> {html: [...], css: [...], js: [...]}"""
    try:
        data = json.loads(request.body) if request.body else {}
        html = data.get('html', '')
        css = data.get('css', '')
        js = data.get('js', '')
        result = validate_all(html, css, js)
        return JsonResponse({
            'html': _errors_to_dict(result['html']),
            'css': _errors_to_dict(result['css']),
            'js': _errors_to_dict(result['js']),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def api_chat(request):
    """API: ответ чат-бота. POST {message, html?, css?, js?, errors?} -> {response}"""
    try:
        data = json.loads(request.body) if request.body else {}
        message = data.get('message', '')
        html = data.get('html', '')
        css = data.get('css', '')
        js = data.get('js', '')
        errors = data.get('errors', [])
        response = get_chat_response(message, html, css, js, errors)
        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'error': str(e), 'response': 'Произошла ошибка. Попробуйте ещё раз.'}, status=400)
