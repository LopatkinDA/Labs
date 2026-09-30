"""
Лабораторная работа № 1, задание 5.

Информационная карточка вычислительного эксперимента:
запрашивает имя исследователя, название эксперимента, число запусков,
длительность одного запуска и комплексный коэффициент; выводит
аккуратно оформленную карточку и диагностическую строку с типами.
"""

name = input("Имя исследователя: ")
experiment = input("Название эксперимента: ")
runs = int(input("Количество запусков: "))
duration = float(input("Длительность одного запуска, с: "))
real_part = float(input("Действительная часть коэффициента: "))
imag_part = float(input("Мнимая часть коэффициента: "))

total_seconds = runs * duration
total_minutes = total_seconds / 60
coeff = complex(real_part, imag_part)
mod_sq = real_part ** 2 + imag_part ** 2
has_runs = bool(runs)

print("=" * 40)
print(f"ЭКСПЕРИМЕНТ: {experiment}")
print(f"Исследователь: {name}")
print(f"Запуски: {runs}")
print(f"Общее время: {total_seconds:.2f} с ({total_minutes:.2f} мин)")
print(f"Коэффициент: {coeff}")
print(f"Квадрат модуля: {mod_sq:.2f}")
print(f"Есть выполненные запуски: {has_runs}")
print("=" * 40)

print("Типы введённых значений:")
print("  name       ->", type(name))
print("  experiment ->", type(experiment))
print("  runs       ->", type(runs))
print("  duration   ->", type(duration))
print("  real_part  ->", type(real_part))
print("  imag_part  ->", type(imag_part))