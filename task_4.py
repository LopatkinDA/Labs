"""
Лабораторная работа № 1, задание 4.
Строки, Unicode, срезы, форматирование.
"""

student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

# 1. Первый и последний символ имени
print("Первый символ:", student[0])
print("Последний символ:", student[-1])

# 2. Срезы: имя и фамилия
first_name = student[:4]
last_name = student[5:]
print("Имя:", first_name)
print("Фамилия:", last_name)

# 3. Регистры
print("Верхний:", student.upper())
print("Нижний:", student.lower())

# 4. Инициалы
initials = student[0] + "." + student[5] + "."
print("Инициалы:", initials)

# 5. Курс в обратном порядке
print("Курс наоборот:", course[::-1])

# 6. Три способа форматирования
percent = completed / total * 100
line_percent = "%s — %s: %d/%d (%.1f%%)" % (
    student, course, completed, total, percent
)
line_format = "{} — {}: {}/{} ({:.1f}%)".format(
    student, course, completed, total, percent
)
line_f = f"{student} — {course}: {completed}/{total} ({percent:.1f}%)"

print(line_percent)
print(line_format)
print(line_f)

# 7. Unicode
symbol = "Я"
print("Символ:", symbol)
print("ord(symbol):", ord(symbol))
print("chr(ord(symbol)):", chr(ord(symbol)))
encoded = symbol.encode("utf-8")
print("encode('utf-8'):", encoded)
print("len(symbol):", len(symbol))
print("len(encoded):", len(encoded))

# 8. Строка неизменяема. Раскомментируйте — получите TypeError:
# symbol[0] = "я"
# TypeError: 'str' object does not support item assignment
