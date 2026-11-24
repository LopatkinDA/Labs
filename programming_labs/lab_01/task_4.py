"""Индексация, срезы, форматирование и Unicode."""
student = 'Анна Смирнова'
course = 'Основы программирования на Python'
completed = 7
total = 10
print('Первый символ:', student[0])
print('Последний символ:', student[-1])
print('Имя:', student[:4])
print('Фамилия:', student[5:])
print(student.upper())
print(student.lower())
print('Инициалы:', student[0] + '.' + student[5] + '.')
print('Курс наоборот:', course[::-1])
percent = completed / total * 100
line = '%s' % student
line += ' — %s' % course
line += ': %d' % completed
line += '/%d' % total
line += ' (%.1f%%)' % percent
print(line)
print('{} — {}: {}/{} ({:.1f}%)'.format(
    student, course, completed, total, percent))
print(f'{student} — {course}: {completed}/{total} ({percent:.1f}%)')
# Прогноз: один символ Я занимает два байта в UTF-8.
symbol = 'Я'
print(symbol, ord(symbol), chr(ord(symbol)))
print(symbol.encode('utf-8'))
print(len(symbol), len(symbol.encode('utf-8')))
# Эта строка вызвала бы TypeError: строки нельзя менять по индексу.
# student[0] = 'О'
