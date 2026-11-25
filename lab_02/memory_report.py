import gc
import sys
import tracemalloc

# Прогноз: список растет ступенями, range занимает меньше памяти.
# Сначала собираем измерения. Печать будет ниже.
rows = []
names = ['empty list', 'list 10', 'tuple 10', 'string 10',
         'int', 'None', 'list 100000', 'range 100000']
for name in names:
    gc.collect()
    tracemalloc.start()
    if name == 'empty list':
        obj = []
    elif name == 'list 10':
        obj = list(range(10))
    elif name == 'tuple 10':
        obj = tuple(range(10))
    elif name == 'string 10':
        obj = 'abcdefghij'
    elif name == 'int':
        obj = 1000
    elif name == 'None':
        obj = None
    elif name == 'list 100000':
        obj = list(range(100000))
    else:
        obj = range(100000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    if name == 'int' or name == 'None':
        count = 1
    else:
        count = len(obj)
    rows.append([name, count, sys.getsizeof(obj), current, peak])
    del obj

numbers = []
old_size = sys.getsizeof(numbers)
growth = [[0, old_size]]
for number in range(100):
    numbers.append(number)
    new_size = sys.getsizeof(numbers)
    if new_size != old_size:
        growth.append([len(numbers), new_size])
        old_size = new_size

ratio = rows[6][4] / rows[7][4]

# Измерения закончены. Теперь выводим сохраненные данные.
print('Прогноз: список растет ступенями; range требует меньше памяти.')
print('Сценарий | Элементов | Размер, Б | Текущая, КиБ | Пиковая, КиБ')
for row in rows:
    print(row[0], row[1], row[2], round(row[3] / 1024, 3),
          round(row[4] / 1024, 3), sep=' | ')
print('Рост списка (длина, байт):', growth)
print('Отношение пиков list/range:', round(ratio, 2))
