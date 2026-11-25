submissions = [
    ('anna', 'lab_01', 5),
    ('boris', 'lab_01', 4),
    ('anna', 'lab_02', 5),
    ('daria', 'lab_01', 3),
    ('boris', 'lab_02', 5),
    ('anna', 'lab_01', 4),
]
students = set()
labs = set()
by_student = {}
best = {}
attempts = {}
completed = {}

for student, lab, score in submissions:
    students.add(student)
    labs.add(lab)
    if student not in by_student:
        by_student[student] = []
    by_student[student].append((lab, score))
    key = (student, lab)
    if key not in best or score > best[key]:
        best[key] = score
    if key not in attempts:
        attempts[key] = 0
    attempts[key] += 1
    if lab not in completed:
        completed[lab] = set()
    completed[lab].add(student)

print('Студенты:', students)
print('Работы:', labs)
print('Попытки студентов:', by_student)
print('Лучшие результаты:', best)
print('Количество попыток:', attempts)
print('Обе работы:', completed['lab_01'] & completed['lab_02'])
assert best[('anna', 'lab_01')] == 5
assert attempts[('anna', 'lab_01')] == 2
assert completed['lab_01'] & completed['lab_02'] == {'anna', 'boris'}

# Добавляем одну запись, старые повторно не обрабатываем.
student, lab, score = 'daria', 'lab_02', 4
submissions.append((student, lab, score))
students.add(student)
labs.add(lab)
if student not in by_student:
    by_student[student] = []
by_student[student].append((lab, score))
key = (student, lab)
if key not in best or score > best[key]:
    best[key] = score
if key not in attempts:
    attempts[key] = 0
attempts[key] += 1
if lab not in completed:
    completed[lab] = set()
completed[lab].add(student)
print('После добавления:', by_student)
print('Теперь обе работы:', completed['lab_01'] & completed['lab_02'])
assert best[('daria', 'lab_02')] == 4
assert attempts[('daria', 'lab_02')] == 1

# Примеры запросов, включая ошибки.
commands = ['student anna', 'best anna lab_01', 'attempts boris lab_02',
            'completed lab_01', 'best nobody lab_99', 'delete anna', 'student', '']
for command in commands:
    print('Запрос:', command)
    parts = command.split()
    if len(parts) == 2 and parts[0] == 'student':
        if parts[1] in by_student:
            print(by_student[parts[1]])
        else:
            print('Нет данных')
    elif len(parts) == 3 and parts[0] == 'best':
        key = (parts[1], parts[2])
        if key in best:
            print(best[key])
        else:
            print('Нет данных')
    elif len(parts) == 3 and parts[0] == 'attempts':
        key = (parts[1], parts[2])
        if key in attempts:
            print(attempts[key])
        else:
            print('Нет данных')
    elif len(parts) == 2 and parts[0] == 'completed':
        if parts[1] in completed:
            print(sorted(completed[parts[1]]))
        else:
            print('Нет данных')
    else:
        print('Неизвестная команда или неверное число аргументов')
