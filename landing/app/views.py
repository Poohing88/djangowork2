from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    version = request.GET.get('from-landing')
    if version == 'original':
        counter_click[version] += 1
    elif version == 'test':
        counter_click[version] += 1
    else:
        pass
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    version = request.GET.get('ab-test-arg')
    if version == 'original':
        counter_show[version] += 1
        return render_to_response('landing.html')
    elif version == 'test':
        counter_show[version] += 1
        return render_to_response('landing_alternate.html')
    else:
        return render_to_response('landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    if counter_show['test']:
        test_conv = float(counter_click['test'] / counter_show['test'])
    else:
        test_conv = 0
    if counter_show['original']:
        original_conv = float(counter_click['original'] / counter_show['original'])
    else:
        original_conv = 0
    return render_to_response('stats.html', context={
        'test_conversion': test_conv,
        'original_conversion': original_conv,
    })
