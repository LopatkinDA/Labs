"""Измерения памяти для задания 5."""
import gc
import sys
import tracemalloc


def measure(name):
    """Создаем один объект и сохраняем результаты измерения."""
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
        obj = list(range(100_000))
    elif name == 'range 100000':
        obj = range(100_000)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if name == 'int' or name == 'None':
        count = 1
    else:
        count = len(obj)
    return {
        'scenario': name,
        'elements': count,
        'outer_bytes': sys.getsizeof(obj),
        'current_bytes': current,
        'peak_bytes': peak,
    }


def collect_measurements():
    names = ['empty list', 'list 10', 'tuple 10', 'string 10',
             'int', 'None', 'list 100000', 'range 100000']
    rows = []
    for name in names:
        rows.append(measure(name))

    # Сохраняем только шаги, на которых изменился размер списка.
    values = []
    old_size = sys.getsizeof(values)
    growth = [(0, old_size)]
    for value in range(100):
        values.append(value)
        new_size = sys.getsizeof(values)
        if new_size != old_size:
            growth.append((len(values), new_size))
            old_size = new_size

    list_peak = rows[6]['peak_bytes']
    range_peak = rows[7]['peak_bytes']
    ratio = list_peak / range_peak
    return {'rows': rows, 'growth': growth, 'peak_ratio': ratio}


def print_measurements(data):
    print('scenario | elements | outer B | current KiB | peak KiB')
    for row in data['rows']:
        current_kib = row['current_bytes'] / 1024
        peak_kib = row['peak_bytes'] / 1024
        print(row['scenario'], row['elements'], row['outer_bytes'],
              round(current_kib, 3), round(peak_kib, 3), sep=' | ')
    print('Рост списка (длина, байт):', data['growth'])
    print('Отношение пиков list/range:', round(data['peak_ratio'], 2))


def main():
    print('Прогноз: список растет ступенями; range занимает меньше памяти.')
    data = collect_measurements()
    assert data['rows'][6]['peak_bytes'] > data['rows'][7]['peak_bytes']
    assert data['rows'][6]['elements'] == 100_000
    assert data['rows'][7]['elements'] == 100_000
    print_measurements(data)


if __name__ == '__main__':
    main()
