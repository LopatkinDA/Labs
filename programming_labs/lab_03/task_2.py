"""Накопление, поиск, сортировка выбором и проверка простоты."""


def statistics(values):
    if not values:
        return None
    total = 0
    even = 0
    low = values[0]
    high = values[0]
    for value in values:
        total += value
        if value < low:
            low = value
        if value > high:
            high = value
        if value % 2 == 0:
            even += 1
    average = total / len(values)
    above = 0
    for value in values:
        if value > average:
            above += 1
    return total, low, high, even, average, above


def linear_search(values, target):
    comparisons = 0
    for index in range(len(values)):
        comparisons += 1
        if values[index] == target:
            return index, comparisons
    return -1, comparisons


def selection_sort(values):
    result = list(values)
    for i in range(len(result) - 1):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        temporary = result[i]
        result[i] = result[smallest]
        result[smallest] = temporary
    return result


def binary_search(values, target):
    left = 0
    right = len(values) - 1
    comparisons = 0
    while left <= right:
        middle = (left + right) // 2
        comparisons += 1
        if values[middle] == target:
            return middle, comparisons
        comparisons += 1
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1, comparisons


def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def main():
    measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
    actual = statistics(measurements)
    assert actual == (144, 7, 21, 4, 14.4, 6)
    assert statistics([]) is None
    print('Сумма, min, max, четные, среднее, выше среднего:', actual)
    target = int(input('Искомое число: '))
    print('Линейный поиск:', target, linear_search(measurements, target))
    assert linear_search(measurements, 18) == (3, 4)
    assert linear_search(measurements, 99) == (-1, 10)
    for number, expected in [(1, False), (2, True), (4, False),
                             (49, False), (97, True), (0, False)]:
        assert is_prime(number) == expected
        print('Простое:', number, is_prime(number))
    sample = [3, 1, 2, 1]
    assert selection_sort(sample) == [1, 1, 2, 3] and sample == [3, 1, 2, 1]
    assert selection_sort([]) == []
    assert binary_search([], 1) == (-1, 0)
    print('n | target | linear comparisons | binary comparisons')
    for n in (10, 100, 1000):
        values = selection_sort(list(range(n - 1, -1, -1)))
        for target in (0, n // 2, n - 1, n):
            linear, c1 = linear_search(values, target)
            binary, c2 = binary_search(values, target)
            assert linear == binary
            print(n, target, c1, c2, sep=' | ')
    print('Проверки задания 2 пройдены')


if __name__ == '__main__':
    main()
