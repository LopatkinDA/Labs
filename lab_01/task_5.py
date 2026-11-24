"""Вводим данные и печатаем карточку вычислительного эксперимента."""
researcher = input('Имя исследователя: ')
experiment = input('Название эксперимента: ')
runs = int(input('Количество запусков: '))
duration = float(input('Длительность запуска в секундах: '))
real = float(input('Действительная часть коэффициента: '))
imag = float(input('Мнимая часть коэффициента: '))
total_seconds = runs * duration
total_minutes = total_seconds / 60
coefficient = complex(real, imag)
squared_module = real ** 2 + imag ** 2
has_runs = bool(runs)
print('=' * 40)
print(f'ЭКСПЕРИМЕНТ: {experiment}')
print(f'Исследователь: {researcher}')
print(f'Запуски: {runs}')
print(f'Общее время: {total_seconds:.2f} с ({total_minutes:.2f} мин)')
print(f'Коэффициент: {coefficient}')
print(f'Квадрат модуля: {squared_module:.2f}')
print(f'Есть выполненные запуски: {has_runs}')
print('=' * 40)
print('Типы ввода:', type(researcher), type(experiment), type(runs),
      type(duration), type(real), type(imag))
