"""Контракты, параметры, LEGB и замыкания."""


def arithmetic_mean(values: list[float]) -> float:
    """Среднее непустого списка; пустой список вызывает ValueError."""
    if not values:
        raise ValueError('Пустой список')
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def normalize_name(name: str) -> str:
    """Убирает лишние пробелы; части имени записывает с прописной буквы."""
    if not name.strip():
        return ''
    parts = name.split()
    result = []
    for part in parts:
        result.append(part.capitalize())
    return ' '.join(result)


def build_report(student: str, results: list[int], *, precision: int = 2,
                 prefix: str = 'Результат') -> str:
    """Отчет о среднем; пустые результаты обозначаются словами «нет данных»."""
    if precision < 0:
        raise ValueError('precision должен быть неотрицательным')
    if not results:
        return f'{prefix}: {normalize_name(student)} — нет данных'
    return f'{prefix}: {normalize_name(student)} — {arithmetic_mean(results):.{precision}f}'


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Очищает теги и сохраняет порядок первых вхождений."""
    result = []
    for tag in tags:
        tag = tag.strip()
        if lowercase:
            tag = tag.lower()
        if tag != '' and tag not in result:
            result.append(tag)
    return tuple(result)


course = 'Основы программирования'


def outer():
    course = 'Локальный курс'

    def inner():
        nonlocal course
        marker = 'обновлен'
        course = course + ': ' + marker
        return course, len(marker)

    return inner()


def bad_add_result(value, results=[]):
    results.append(value)
    return results


def add_result(value, results=None):
    if results is None:
        results = []
    # Копирование также защищает явно переданный список от изменения.
    new_results = results.copy()
    new_results.append(value)
    return new_results


def apply_to_results(operation, values):
    result = []
    for value in values:
        result.append(operation(value))
    return result


def make_threshold_checker(threshold):
    def check(value):
        return value >= threshold
    return check


def double(value):
    return value * 2


assert arithmetic_mean([1.0, 3.0]) == 2.0
assert arithmetic_mean([5.0]) == 5.0
assert arithmetic_mean([-2.0, 2.0]) == 0.0
try:
    arithmetic_mean([])
except ValueError:
    pass
else:
    raise AssertionError('Ожидался ValueError')
assert normalize_name('  иВАН   иВАНОВ ') == 'Иван Иванов'
assert normalize_name('') == ''
assert normalize_name(' АННА ') == 'Анна'
assert build_report('анна', [80, 90]) == 'Результат: Анна — 85.00'
assert build_report('борис', [], prefix='Итог') == 'Итог: Борис — нет данных'
assert build_report(student='дарья', results=[91], precision=0) == 'Результат: Дарья — 91'
assert collect_tags(' Python ', 'python', '', 'IT') == ('python', 'it')
assert collect_tags('A', 'a', lowercase=False) == ('A', 'a')
assert collect_tags() == ()
values = [80, 90]
before = values.copy()
arguments = ['анна', values]
options = {'precision': 1, 'prefix': 'Итог'}
print(build_report(*arguments, **options))
assert values == before
print('Теги:', collect_tags(' Python ', 'python', ' IT '))
print('LEGB:', outer(), 'global:', course)
assert course == 'Основы программирования'
first = bad_add_result(1)
second = bad_add_result(2)
assert first is second and first == [1, 2]
print('Общий default:', first, second)
assert add_result(1) == [1] and add_result(2) == [2]
assert add_result(3, values) == [80, 90, 3] and values == before
print('Исправлено:', add_result(1), add_result(2))
print('Именованная функция:', apply_to_results(double, [1, 2, 3]))
print('lambda:', apply_to_results(lambda x: x + 5, [1, 2, 3]))
assert apply_to_results(double, [1, 2]) == [2, 4]
assert apply_to_results(lambda x: x + 5, [1, 2]) == [6, 7]
check60 = make_threshold_checker(60)
check90 = make_threshold_checker(90)
assert check60(75) and not check90(75)
assert check60(60) and check90(90)
print('Пороги 60 и 90 для 75:', check60(75), check90(75))
print('Проверки задания 4 пройдены')
