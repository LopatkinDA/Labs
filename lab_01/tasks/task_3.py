"""Проверяем числовые операции и преобразования."""
import math

x = 17
y = 5
# Прогноз: только обычное деление этих int дает float.
print('+', x + y, type(x + y))
print('-', x - y, type(x - y))
print('*', x * y, type(x * y))
print('/', x / y, type(x / y))
print('//', x // y, type(x // y))
print('%', x % y, type(x % y))
print('**', x ** y, type(x ** y))
print('Большое целое:', 2 ** 1000)
# Прогноз: точное равенство не выполнится, isclose вернет True.
result = 0.1 + 0.2
print('0.1 + 0.2:', result)
print('== 0.3:', result == 0.3)
print('Разность:', result - 0.3)
print('isclose:', math.isclose(result, 0.3))
print(int('42'), type(int('42')))
print(float('3.14'), type(float('3.14')))
print(str(2026), type(str(2026)))
print(bool(0), type(bool(0)))
print(bool(-1), type(bool(-1)))
print(bool(''), type(bool('')))
print(bool('False'), type(bool('False')))
coefficient = complex(2, -3)
print(coefficient, type(coefficient))
print('Действительная часть:', coefficient.real)
print('Мнимая часть:', coefficient.imag)
print('int(42.9):', int(42.9))
