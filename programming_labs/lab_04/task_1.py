"""Изучаем iter, next и простые аналоги enumerate и zip."""
from task_2 import StepRange


def consume(iterable) -> list:
    """Собираем элементы вручную, пока next не вызовет StopIteration."""
    iterator = iter(iterable)
    result = []
    while True:
        try:
            value = next(iterator)
        except StopIteration:
            break
        result.append(value)
    return result


def my_enumerate(iterable, start=0):
    """Лениво выдаем пары индекс и значение."""
    index = start
    for value in iterable:
        yield index, value
        index += 1


def my_zip(first, second):
    """Останавливаемся при исчерпании любого источника."""
    left = iter(first)
    right = iter(second)
    while True:
        try:
            a = next(left)
            b = next(right)
        except StopIteration:
            return
        yield a, b


def main():
    values = [10, 20, 30]
    iterator = iter(values)
    print(iterator is values)
    print(iter(iterator) is iterator)
    print(next(iterator), next(iterator), next(iterator))
    # next(iterator)  # StopIteration: четвертого элемента нет.
    try:
        next(iterator)
    except StopIteration:
        print('Четвертый next: StopIteration')
    assert consume(values) == [10, 20, 30]
    assert consume((1, 2)) == [1, 2]
    assert consume('abc') == ['a', 'b', 'c']
    assert consume(range(3)) == [0, 1, 2]
    partial = iter(values)
    next(partial)
    assert consume(partial) == [20, 30]
    assert consume(partial) == []
    print('Повторный список:', consume(values), consume(values))
    print('Исчерпанный итератор:', consume(partial))
    assert list(my_enumerate([10, 20], 1)) == [(1, 10), (2, 20)]
    assert list(my_enumerate('ab')) == [(0, 'a'), (1, 'b')]
    assert list(my_enumerate(x * 2 for x in [1, 2])) == [(0, 2), (1, 4)]
    assert list(my_enumerate(StepRange(2, 8, 3))) == [(0, 2), (1, 5)]
    assert list(my_zip([1, 2, 3], 'ab')) == [(1, 'a'), (2, 'b')]
    assert list(my_zip('ab', 'XY')) == [('a', 'X'), ('b', 'Y')]
    assert list(my_zip((x for x in [1, 2]), 'ab')) == [(1, 'a'), (2, 'b')]
    assert list(my_zip(StepRange(0, 3, 1), 'ab')) == [(0, 'a'), (1, 'b')]
    assert list(my_zip([], 'ab')) == []
    print('consume, my_enumerate, my_zip: проверки пройдены')


if __name__ == '__main__':
    main()
