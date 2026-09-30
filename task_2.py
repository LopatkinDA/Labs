"""
Лабораторная работа № 1, задание 2.
Имена, объекты, сравнение == и is.
"""

a = 1000
b = a
c = int("1000")

# Прогноз (записан до запуска):
#   a == b : True  — значения равны
#   a is b : True  — b ссылается на тот же объект, что и a
#   a == c : True  — значения равны
#   a is c : False — c — новый объект, созданный вызовом int("1000")

print("Типы:", type(a), type(b), type(c))
print("Идентификаторы:", id(a), id(b), id(c))
print("a == b:", a == b)
print("a is b:", a is b)
print("a == c:", a == c)
print("a is c:", a is c)

# Изменяем c на None и проверяем корректно — через is
c = None
print("c is None:", c is None)

# --- Фрагмент со строками ---
first = "python"
second = "py" + "thon"

# Прогноз:
#   first == second : True
#   first is second : True — но это деталь реализации CPython
#   (интернирование строковых литералов), полагаться на это нельзя.

print(first == second)
print(first is second)