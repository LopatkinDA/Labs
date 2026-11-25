# Балл, тип работы, пропуски.
records = [
    (0, 'exam', 0),
    (59, 'project', 3),
    (60, 'practice', 0),
    (74, 'exam', 3),
    (75, 'project', 0),
    (89, 'practice', 3),
    (90, 'exam', 0),
    (100, 'project', 3),
    (90, 'exam', 4),
    (60, 'practice', 5),
]
before = records.copy()
counts = {'недостаточный': 0, 'удовлетворительный': 0,
          'хороший': 0, 'отличный': 0}

# Одна запись, десять записей группы и дополнительные проверки.
checks = [(90, 'exam', 0)]
checks += records
checks += [(-1, 'exam', 0), (101, 'exam', 0),
           (80, 'exam', -1), (80, 'exam', 6),
           (80, 'other', 0)]
expected = ['отличный',
 'недостаточный',
 'недостаточный',
 'удовлетворительный',
 'удовлетворительный',
 'хороший',
 'хороший',
 'отличный',
 'отличный',
 'хороший',
 'недостаточный',
 '',
 '',
 '',
 '',
 'хороший']
for i in range(len(checks)):
    score, work_type, absences = checks[i]
    print('Данные:', score, work_type, absences)
    if score < 0 or score > 100:
        print('Ошибка: балл должен быть от 0 до 100')
    elif absences < 0 or absences > 5:
        print('Ошибка: пропуски должны быть от 0 до 5')
    else:
        if score >= 90:
            level = 'отличный'
        elif score >= 75:
            level = 'хороший'
        elif score >= 60:
            level = 'удовлетворительный'
        else:
            level = 'недостаточный'
        if absences > 3:
            if level == 'отличный':
                level = 'хороший'
            elif level == 'хороший':
                level = 'удовлетворительный'
            elif level == 'удовлетворительный':
                level = 'недостаточный'
        match work_type:
            case 'exam':
                description = 'экзаменационная работа'
            case 'project':
                description = 'проектная работа'
            case 'practice':
                description = 'практическая работа'
            case _:
                description = 'неизвестный тип работы'
        print(description + '; уровень: ' + level)
        print('Ожидалось:', expected[i])
        assert level == expected[i]
        # В сводку входят только десять записей группы.
        if 1 <= i <= 10:
            counts[level] += 1
print('Сводка:', counts)
assert counts == {'недостаточный': 3, 'удовлетворительный': 2,
                  'хороший': 3, 'отличный': 2}

assert records == before
