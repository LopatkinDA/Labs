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
    rating = summaries.copy()
    for i in range(len(rating) - 1):
        for j in range(len(rating) - 1 - i):
            left = rating[j]['mean']
            right = rating[j + 1]['mean']
            if left is None:
                left = -1
            if right is None:
                right = -1
            if left < right:
                temporary = rating[j]
                rating[j] = rating[j + 1]
                rating[j + 1] = temporary
    return {
        'student_count': len(students),
        'result_count': count,
        'mean': average,
        'categories': categories,
        'leaders': find_top_students(students),
        'rating': rating,
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


original = deepcopy(students)
summaries = []
for name in students:
    summaries.append(student_summary(name, students[name]))
group = group_summary(students)
print(format_report(summaries, group))
assert students == original
assert group['mean'] == 1032 / 13
assert group['leaders'] == ['Дарья']

# Еще пять сценариев вместе с обычной группой дают шесть проверок.
one = group_summary({'А': [80]})
assert one['mean'] == 80
print('Один студент:', one['mean'], one['leaders'])

tied = group_summary({'А': [80, 100], 'Б': [90]})
assert tied['leaders'] == ['А', 'Б']
print('Два лидера:', tied['leaders'])

empty = group_summary({})
assert empty['mean'] is None
print('Пустая группа:', empty['mean'], empty['leaders'])

no_results = group_summary({'А': [], 'Б': [60]})
assert no_results['mean'] == 60
assert student_summary('А', [])['category'] == 'нет данных'
print('Студент без оценок:', no_results['mean'], no_results['leaders'])

boundaries = {'0': [0], '59': [59], '60': [60], '74': [74],
              '75': [75], '89': [89], '90': [90], '100': [100]}
border_group = group_summary(boundaries)
assert border_group['mean'] == 547 / 8
print('Границы:', border_group['mean'], border_group['leaders'])
for name in boundaries:
    print(name, classify(boundaries[name][0]))

assert minimum([]) is None
assert maximum([]) is None
assert mean([]) is None
