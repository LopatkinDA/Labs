import sys
import tracemalloc

print('Размеры объектов в байтах:')
print('Пустой список:', sys.getsizeof([]))
print('Список 10 чисел:', sys.getsizeof(list(range(10))))
print('Кортеж 10 чисел:', sys.getsizeof(tuple(range(10))))
print('Строка 10 символов:', sys.getsizeof('abcdefghij'))
print('Число:', sys.getsizeof(1000))
print('None:', sys.getsizeof(None))

# Прогноз: размер списка растет не после каждого append.
numbers = []
old_size = sys.getsizeof(numbers)
print(len(numbers), old_size)
for number in range(100):
    numbers.append(number)
    new_size = sys.getsizeof(numbers)
    if new_size != old_size:
        print(len(numbers), new_size)
        old_size = new_size

# Прогноз: list(range(100000)) занимает больше памяти, чем range.
tracemalloc.start()
numbers = list(range(100000))
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print('Список: текущая память, КиБ:', current / 1024)
print('Список: пиковая память, КиБ:', peak / 1024)
del numbers

tracemalloc.start()
numbers = range(100000)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print('range: текущая память, КиБ:', current / 1024)
print('range: пиковая память, КиБ:', peak / 1024)
