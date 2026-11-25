measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

# Первый проход: сумма, минимум, максимум и четные числа.
total = 0
low = measurements[0]
high = measurements[0]
even = 0
for number in measurements:
    total += number
    if number < low:
        low = number
    if number > high:
        high = number
    if number % 2 == 0:
        even += 1

# Второй проход: числа выше среднего.
average = total / len(measurements)
above = 0
for number in measurements:
    if number > average:
        above += 1
print('Сумма:', total)
print('Минимум:', low)
print('Максимум:', high)
print('Четных:', even)
print('Среднее:', average)
print('Выше среднего:', above)
assert (total, low, high, even, average, above) == (144, 7, 21, 4, 14.4, 6)

# Линейный поиск останавливается на первом совпадении.
target = int(input('Искомое число: '))
found = -1
comparisons = 0
for i in range(len(measurements)):
    comparisons += 1
    if measurements[i] == target:
        found = i
        break
print('Индекс:', found)
print('Сравнений:', comparisons)

# Для 0 и 1 результат сразу False.
for number in [0, 1, 2, 4, 49, 97]:
    prime = number >= 2
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            prime = False
            break
        divisor += 1
    print('Простое число:', number, prime)
    if number == 2 or number == 97:
        assert prime
    else:
        assert not prime

# Сортировка выбором копии списка.
sample = [3, 1, 2, 1]
result = sample.copy()
for i in range(len(result) - 1):
    smallest = i
    for j in range(i + 1, len(result)):
        if result[j] < result[smallest]:
            smallest = j
    temporary = result[i]
    result[i] = result[smallest]
    result[smallest] = temporary
print('После сортировки:', result)
assert result == [1, 1, 2, 3]
assert sample == [3, 1, 2, 1]

# Сравниваем два поиска на одинаковых отсортированных списках.
print('n | цель | линейный | бинарный')
for n in [10, 100, 1000]:
    numbers = list(range(n - 1, -1, -1))
    for i in range(len(numbers) - 1):
        smallest = i
        for j in range(i + 1, len(numbers)):
            if numbers[j] < numbers[smallest]:
                smallest = j
        temporary = numbers[i]
        numbers[i] = numbers[smallest]
        numbers[smallest] = temporary
    for target in [0, n // 2, n - 1, n]:
        linear_index = -1
        linear_count = 0
        for i in range(len(numbers)):
            linear_count += 1
            if numbers[i] == target:
                linear_index = i
                break
        binary_index = -1
        binary_count = 0
        left = 0
        right = len(numbers) - 1
        while left <= right:
            middle = (left + right) // 2
            binary_count += 1
            if numbers[middle] == target:
                binary_index = middle
                break
            binary_count += 1
            if numbers[middle] < target:
                left = middle + 1
            else:
                right = middle - 1
        assert linear_index == binary_index
        if target == n:
            assert binary_index == -1
        else:
            assert binary_index == target
        print(n, target, linear_count, binary_count, sep=' | ')
