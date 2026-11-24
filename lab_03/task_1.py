"""Условия, match и обработка группы записей."""
LEVELS = ('недостаточный', 'удовлетворительный', 'хороший', 'отличный')


def classify_record(score: int, work_type: str, absences: int) -> tuple[str, str]:
    """Возвращает уровень и пояснение; ошибка диапазона прекращает классификацию."""
    if not 0 <= score <= 100:
        return '', 'Ошибка: результат вне диапазона 0..100'
    elif not 0 <= absences <= 5:
        return '', 'Ошибка: пропуски вне диапазона 0..5'
    else:
        if score >= 90:
            index = 3
        elif score >= 75:
            index = 2
        elif score >= 60:
            index = 1
        else:
            index = 0
    if absences > 3 and index > 0:
        index -= 1
    match work_type:
        case 'exam':
            description = 'экзаменационная работа'
        case 'project':
            description = 'проектная работа'
        case 'practice':
            description = 'практическая работа'
        case _:
            description = 'неизвестный тип работы'
    return LEVELS[index], description


def main():
    cases = [(0, 'exam', 0, LEVELS[0]), (59, 'project', 3, LEVELS[0]),
             (60, 'practice', 0, LEVELS[1]), (74, 'exam', 3, LEVELS[1]),
             (75, 'project', 0, LEVELS[2]), (89, 'practice', 3, LEVELS[2]),
             (90, 'exam', 0, LEVELS[3]), (100, 'project', 3, LEVELS[3]),
             (90, 'exam', 4, LEVELS[2]), (60, 'practice', 5, LEVELS[0]),
             (-1, 'exam', 0, ''), (101, 'exam', 0, ''),
             (80, 'exam', -1, ''), (80, 'exam', 6, ''),
             (80, 'other', 0, LEVELS[2])]
    for score, kind, absences, expected in cases:
        actual, description = classify_record(score, kind, absences)
        assert actual == expected
        print((score, kind, absences), 'ожидалось:', expected,
              'получено:', actual, description)
    records = []
    for score, kind, absences, expected in cases[:10]:
        records.append((score, kind, absences))
    before = records.copy()
    counts = {}
    for level in LEVELS:
        counts[level] = 0
    for score, kind, absences in records:
        level, description = classify_record(score, kind, absences)
        counts[level] += 1
        print(score, kind, absences, ':', description, '; уровень', level)
    assert records == before
    assert counts == {LEVELS[0]: 3, LEVELS[1]: 2, LEVELS[2]: 3, LEVELS[3]: 2}
    print('Сводка:', counts)
    print('Проверки задания 1 пройдены')


if __name__ == '__main__':
    main()
