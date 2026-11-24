"""Ленивый конвейер измерений и сравнение памяти."""
import gc
import tracemalloc
from collections import deque
from collections.abc import Iterable, Iterator


def read_measurements(lines: Iterable[str]) -> Iterator[float]:
    """Преобразуем непустые строки в числа."""
    for line in lines:
        if line.strip() != '':
            yield float(line)


def filter_range(values: Iterable[float], minimum: float,
                 maximum: float) -> Iterator[float]:
    """Оставляем числа из закрытого диапазона."""
    if minimum > maximum:
        raise ValueError('Минимум больше максимума')
    for value in values:
        if minimum <= value <= maximum:
            yield value


def moving_average(values: Iterable[float], window_size: int) -> Iterator[float]:
    """Храним только последнее окно и выдаем его среднее."""
    if window_size <= 0:
        raise ValueError('Размер окна должен быть положительным')
    window = deque()
    total = 0.0
    for value in values:
        window.append(value)
        total += value
        if len(window) > window_size:
            total -= window.popleft()
        if len(window) == window_size:
            yield total / window_size


def take(n: int, iterable: Iterable) -> Iterator:
    """Выдаем не больше n элементов, не читая лишний."""
    if n < 0:
        raise ValueError('n не может быть отрицательным')
    iterator = iter(iterable)
    for _ in range(n):
        try:
            value = next(iterator)
        except StopIteration:
            return
        yield value


def drop(n: int, iterable: Iterable) -> Iterator:
    """Пропускаем первые n элементов."""
    if n < 0:
        raise ValueError('n не может быть отрицательным')
    iterator = iter(iterable)
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            return
    yield from iterator


def batch(iterable: Iterable, size: int) -> Iterator[list]:
    """Выдаем пакеты, последний может быть неполным."""
    if size <= 0:
        raise ValueError('Размер пакета должен быть положительным')
    packet = []
    for value in iterable:
        packet.append(value)
        if len(packet) == size:
            yield packet
            packet = []
    if packet:
        yield packet


def pipeline(lines: Iterable[str]) -> Iterator[float]:
    """Соединяем три генератора без промежуточных списков."""
    numbers = read_measurements(lines)
    filtered = filter_range(numbers, 0, 20)
    return moving_average(filtered, 3)


def memory_peak(lazy: bool) -> tuple[int, float]:
    """Сравниваем одинаковые данные и одинаковый итог."""
    gc.collect()
    tracemalloc.start()
    lines = (str(i % 20) for i in range(100_000))
    if lazy:
        result = pipeline(lines)
    else:
        raw = list(lines)
        numbers = list(read_measurements(raw))
        filtered = list(filter_range(numbers, 0, 20))
        result = list(moving_average(filtered, 3))
    total = 0.0
    for value in result:
        total += value
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak, total


def main() -> None:
    """Проверяем ленивость, исчерпание, включения и память."""
    raw_lines = ['10.0', '', '12.5', '100.0', '11.5', '13.0', '9.5']
    original = raw_lines.copy()
    stream = pipeline(raw_lines)
    print('Первые два:', next(stream), next(stream))
    print('Остаток:', list(stream))
    assert list(stream) == []
    assert list(pipeline(raw_lines)) == [34 / 3, 37 / 3, 34 / 3]
    assert raw_lines == original
    squares = [x * x for x in range(1, 21) if x % 2 == 0]
    lengths = {len(line) for line in raw_lines if line != ''}
    mapping = {x: x * x for x in range(1, 11)}
    total = sum(x * x for x in range(100_000))
    print('Включения:', squares, lengths, mapping)
    print('Сумма квадратов:', total)
    packets = list(batch(take(3, drop(1, pipeline(raw_lines))), 2))
    print('Пакеты:', packets)
    assert packets == [[37 / 3, 34 / 3]]
    assert list(take(0, range(5))) == []
    assert list(drop(10, range(3))) == []
    assert list(batch(range(5), 2)) == [[0, 1], [2, 3], [4]]
    for generator in [moving_average([], 0), batch([], 0), take(-1, []), drop(-1, [])]:
        try:
            next(generator)
        except ValueError as error:
            print('Проверка ошибки:', error)
        else:
            raise AssertionError('Ожидался ValueError')
    lazy_peak, lazy_total = memory_peak(True)
    list_peak, list_total = memory_peak(False)
    assert lazy_total == list_total
    assert lazy_peak < list_peak
    print('Пики, байт: lazy =', lazy_peak, 'list =', list_peak)


if __name__ == '__main__':
    main()
