"""Простой анализатор результатов студентов."""
from copy import deepcopy

students = {
    'Анна': [78, 91, 84, 88],
    'Борис': [60, 72, 68],
    'Дарья': [95, 93, 97, 90],
    'Илья': [55, 61],
}


def mean(values):
    """Среднее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    total = 0
    for value in values:
        total += value
    return total / len(values)


def minimum(values):
    """Наименьшее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values):
    """Наибольшее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def classify(score):
    """Определяем категорию среднего балла от 0 до 100."""
    if score is None:
        return 'нет данных'
    if score >= 90:
        return 'отличный'
    elif score >= 75:
        return 'хороший'
    elif score >= 60:
        return 'удовлетворительный'
    else:
        return 'недостаточный'


def student_summary(name, results):
    """Собираем показатели одного студента в словарь."""
    average = mean(results)
    return {
        'name': name,
        'count': len(results),
        'mean': average,
        'minimum': minimum(results),
        'maximum': maximum(results),
        'category': classify(average),
    }


def rank(summaries):
    """Сортируем копию списка сводок по убыванию среднего балла."""
    result = summaries.copy()
    # Пузырьковая сортировка: сравниваем соседние записи.
    for i in range(len(result) - 1):
        for j in range(len(result) - 1 - i):
            left = result[j]['mean']
            right = result[j + 1]['mean']
            # Студенты без оценок должны попасть в конец.
            if left is None:
                left = -1
            if right is None:
                right = -1
            if left < right:
                temporary = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temporary
    return result


def find_top_students(students):
    """Находим всех студентов с самым высоким средним баллом."""
    best = None
    leaders = []
    for name in students:
        average = mean(students[name])
        if average is None:
            continue
        if best is None or average > best:
            best = average
            leaders = [name]
        elif average == best:
            leaders.append(name)
    return leaders


def group_summary(students):
    """Собираем общую статистику, лидеров и рейтинг группы."""
    summaries = []
    categories = {
        'недостаточный': 0,
        'удовлетворительный': 0,
        'хороший': 0,
        'отличный': 0,
        'нет данных': 0,
    }
    total = 0
    count = 0
    for name in students:
        values = students[name]
        summary = student_summary(name, values)
        summaries.append(summary)
        categories[summary['category']] += 1
        for value in values:
            total += value
            count += 1
    if count == 0:
        average = None
    else:
        average = total / count
    return {
        'student_count': len(students),
        'result_count': count,
        'mean': average,
        'categories': categories,
        'leaders': find_top_students(students),
        'rating': rank(summaries),
    }


def format_report(student_data, group_data):
    """Формируем текст из готовых сводок."""
    lines = []
    for row in student_data:
        if row['mean'] is None:
            line = row['name'] + ': нет данных'
        else:
            average = round(row['mean'], 2)
            line = f"{row['name']}: среднее {average}; "
            line += f"min {row['minimum']}; max {row['maximum']}; "
            line += row['category']
        lines.append(line)
    if group_data['mean'] is None:
        lines.append('Среднее группы: нет данных')
    else:
        average = round(group_data['mean'], 2)
        lines.append('Среднее группы: ' + str(average))
    if len(group_data['leaders']) == 0:
        lines.append('Лидеры: нет')
    else:
        lines.append('Лидеры: ' + ', '.join(group_data['leaders']))
    lines.append('Категории: ' + str(group_data['categories']))
    names = []
    for row in group_data['rating']:
        names.append(row['name'])
    lines.append('Рейтинг: ' + ', '.join(names))
    return '\n'.join(lines)


def main():
    original = deepcopy(students)
    summaries = []
    for name in students:
        summaries.append(student_summary(name, students[name]))
    group = group_summary(students)
    print(format_report(summaries, group))
    assert students == original
    assert group['mean'] == 1032 / 13
    assert group['leaders'] == ['Дарья']

    # Название сценария, данные, ожидаемое среднее, ожидаемые лидеры.
    boundaries = {
        '0': [0], '59': [59], '60': [60], '74': [74],
        '75': [75], '89': [89], '90': [90], '100': [100],
    }
    checks = [
        ('обычная группа', students, 1032 / 13, ['Дарья']),
        ('один студент', {'А': [80]}, 80, ['А']),
        ('равные лидеры', {'А': [80, 100], 'Б': [90]}, 90, ['А', 'Б']),
        ('пустая группа', {}, None, []),
        ('нет результатов', {'А': [], 'Б': [60]}, 60, ['Б']),
        ('все без результатов', {'А': []}, None, []),
        ('границы', boundaries, 547 / 8, ['100']),
    ]
    for label, data, expected_mean, expected_leaders in checks:
        before = deepcopy(data)
        actual = group_summary(data)
        assert actual['mean'] == expected_mean
        assert actual['leaders'] == expected_leaders
        assert data == before
        print(label, '=>', actual['mean'], actual['leaders'], 'OK')

    category_checks = [
        (0, 'недостаточный'), (59, 'недостаточный'),
        (60, 'удовлетворительный'), (74, 'удовлетворительный'),
        (75, 'хороший'), (89, 'хороший'),
        (90, 'отличный'), (100, 'отличный'),
    ]
    for score, expected in category_checks:
        assert classify(score) == expected
    assert mean([]) is None
    assert minimum([]) is None
    assert maximum([]) is None
    assert minimum([2, -1, 4]) == -1
    assert maximum([2, -1, 4]) == 4
    assert mean([2, 4]) == 3
    assert student_summary('А', [])['category'] == 'нет данных'
    names = []
    for row in group['rating']:
        names.append(row['name'])
    assert names == ['Дарья', 'Анна', 'Борис', 'Илья']
    empty_student_group = group_summary({'А': [], 'Б': [60]})
    assert empty_student_group['rating'][0]['name'] == 'Б'
    assert empty_student_group['rating'][1]['name'] == 'А'
    tied_group = group_summary({'А': [90], 'Б': [90]})
    assert tied_group['rating'][0]['name'] == 'А'
    assert tied_group['rating'][1]['name'] == 'Б'
    empty_report = format_report(
        [student_summary('А', [])], group_summary({'А': []})
    )
    assert 'нет данных' in empty_report
    print('Проверки задания 5 пройдены')


if __name__ == '__main__':
    main()
