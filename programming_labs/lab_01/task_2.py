"""Сравниваем значения и объекты."""
# Прогноз: True, True, True, False для четырех сравнений ниже.
a = 1000
b = a
c = int('1000')
print('Типы:', type(a), type(b), type(c))
print('Идентификаторы:', id(a), id(b), id(c))
print('a == b:', a == b)
print('a is b:', a is b)
print('a == c:', a == c)
print('a is c:', a is c)
c = None
print('c is None:', c is None)
# Прогноз: значения строк равны; is зависит от работы компилятора.
first = 'python'
second = 'py' + 'thon'
print(first == second)
print(first is second)
