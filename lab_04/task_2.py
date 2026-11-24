"""Повторно обходимый диапазон без хранения списка чисел."""


class StepRangeIterator:
    """Хранит состояние одного обхода."""

    def __init__(self, start: int, stop: int, step: int) -> None:
        """Запоминаем текущее число, границу и шаг."""
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> 'StepRangeIterator':
        """Итератор возвращает себя."""
        return self

    def __next__(self) -> int:
        """Выдаем число и сдвигаем текущее значение."""
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        if self.step < 0 and self.current <= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


class StepRange:
    """Хранит только start, stop и ненулевой step."""

    def __init__(self, start: int, stop: int, step: int) -> None:
        """Создаем диапазон, не включая stop."""
        if step == 0:
            raise ValueError('Шаг не может быть нулевым')
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> StepRangeIterator:
        """Для каждого обхода создаем независимый итератор."""
        return StepRangeIterator(self.start, self.stop, self.step)

    def __len__(self) -> int:
        """Вычисляем число элементов без перебора."""
        if self.step > 0:
            distance = self.stop - self.start
        else:
            distance = self.start - self.stop
        if distance <= 0:
            return 0
        step = abs(self.step)
        return (distance + step - 1) // step

    def __contains__(self, value: int) -> bool:
        """Проверяем границы и кратность шага."""
        if not isinstance(value, int):
            return False
        if self.step > 0:
            inside = self.start <= value < self.stop
        else:
            inside = self.stop < value <= self.start
        return inside and (value - self.start) % self.step == 0

    def __repr__(self) -> str:
        """Показываем параметры диапазона."""
        return f'StepRange({self.start}, {self.stop}, {self.step})'


def main() -> None:
    """Проверяем шаги, границы и независимость обходов."""
    for start, stop, step, expected in [
        (2, 11, 3, [2, 5, 8]), (0, 5, 1, [0, 1, 2, 3, 4]),
        (5, 0, -1, [5, 4, 3, 2, 1]), (0, 0, 1, []), (0, 5, -1, []),
    ]:
        numbers = StepRange(start, stop, step)
        assert list(numbers) == expected
        assert len(numbers) == len(expected)
        assert list(numbers) == expected
        print(repr(numbers), list(numbers), len(numbers))
    try:
        StepRange(0, 5, 0)
    except ValueError as error:
        print(type(error).__name__, error)
    else:
        raise AssertionError('Нулевой шаг должен отклоняться')
    numbers = StepRange(2, 11, 3)
    first = iter(numbers)
    second = iter(numbers)
    for iterator in [first, second, first, second]:
        print('Выдано:', next(iterator), 'состояние:', first.current, second.current)
    assert first.current == second.current == 8
    assert 5 in numbers and 6 not in numbers and 11 not in numbers
    assert 3 in StepRange(5, 0, -1)
    large = StepRange(0, 1_000_000, 1)
    target = 999_999
    comparisons = 0
    for value in large:
        comparisons += 1
        if value == target:
            break
    print('Перебор:', comparisons, 'проверок; contains:', target in large)
    print('contains: две проверки границ, остаток от деления и сравнение с 0')
    assert comparisons == 1_000_000


if __name__ == '__main__':
    main()
