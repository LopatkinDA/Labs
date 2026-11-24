"""Индексы результатов и безопасный разбор запросов."""
SUBMISSIONS = [('anna', 'lab_01', 5), ('boris', 'lab_01', 4),
               ('anna', 'lab_02', 5), ('daria', 'lab_01', 3),
               ('boris', 'lab_02', 5), ('anna', 'lab_01', 4)]


def empty_index():
    return {'students': set(), 'labs': set(), 'by_student': {},
            'best': {}, 'attempts': {}, 'completed': {}}


def add(index, record):
    student, lab, score = record
    key = student, lab
    index['students'].add(student)
    index['labs'].add(lab)
    if student not in index['by_student']:
        index['by_student'][student] = []
    index['by_student'][student].append((lab, score))
    if key not in index['best'] or score > index['best'][key]:
        index['best'][key] = score
    if key not in index['attempts']:
        index['attempts'][key] = 0
    index['attempts'][key] += 1
    if lab not in index['completed']:
        index['completed'][lab] = set()
    index['completed'][lab].add(student)


def query(index, command):
    parts = command.split()
    if len(parts) == 2 and parts[0] == 'student':
        name = parts[1]
        if name in index['by_student']:
            return str(index['by_student'][name])
        return 'Нет данных'
    elif len(parts) == 3 and parts[0] == 'best':
        key = (parts[1], parts[2])
        if key in index['best']:
            return str(index['best'][key])
        return 'Нет данных'
    elif len(parts) == 3 and parts[0] == 'attempts':
        key = (parts[1], parts[2])
        if key in index['attempts']:
            return str(index['attempts'][key])
        return 'Нет данных'
    elif len(parts) == 2 and parts[0] == 'completed':
        lab = parts[1]
        if lab in index['completed']:
            return str(sorted(index['completed'][lab]))
        return 'Нет данных'
    return 'Неизвестная команда или неверное число аргументов'


def main():
    index = empty_index()
    for record in SUBMISSIONS:
        add(index, record)
    print('Индексы до добавления:', index)
    both = index['completed']['lab_01'] & index['completed']['lab_02']
    print('Обе работы:', sorted(both))
    assert both == {'anna', 'boris'}
    assert index['best'][('anna', 'lab_01')] == 5
    assert index['attempts'][('anna', 'lab_01')] == 2
    add(index, ('daria', 'lab_02', 4))
    print('После добавления daria lab_02 4:', index)
    assert index['attempts'][('daria', 'lab_02')] == 1
    for command in ('student anna', 'best anna lab_01', 'attempts boris lab_02',
                    'completed lab_01', 'best nobody lab_99', 'delete anna',
                    'student', ''):
        print(command, '=>', query(index, command))
    assert query(index, 'best anna lab_01') == '5'
    assert query(index, 'best nobody lab_99') == 'Нет данных'
    assert query(index, 'student').startswith('Неизвестная')
    print('Проверки задания 3 пройдены')


if __name__ == '__main__':
    main()
