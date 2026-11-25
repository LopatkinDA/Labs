"""Циклы и явная сборка; автоматическая сборка восстановлена в finally."""
import gc


print('GC включен:', gc.isenabled())
print('Пороги:', gc.get_threshold())
print('Статистика:', gc.get_stats())
# Прогноз: цикл недостижим после del, его собирает gc.collect().
gc.collect()
gc.disable()
try:
    first, second = [], []
    first.append(second)
    second.append(first)
    print(first[0] is second, second[0] is first)
    ids = (id(first), id(second))
    print('Идентификаторы:', ids)
    del first, second
    print('Собрано для пары:', gc.collect())
    # Прогноз: пять самоссылочных списков будут собраны вручную.
    for _ in range(5):
        cycle = []
        cycle.append(cycle)
        del cycle
    print('Собрано для пяти циклов:', gc.collect())
    # Прогноз графа: цикл A-B-C исчезнет; D останется доступен.
    before = gc.collect()
    a = {'name': 'A', 'edges': []}
    b = {'name': 'B', 'edges': []}
    c = {'name': 'C', 'edges': []}
    independent = {'name': 'D', 'edges': []}
    a['edges'].append(b)
    b['edges'].append(c)
    c['edges'].append(a)
    print('Связи: A -> B -> C -> A; D -> []')
    del a, b, c
    after = gc.collect()
    print('Сборка до графа:', before, 'после удаления:', after)
    assert independent == {'name': 'D', 'edges': []}
    print('Независимый узел:', independent)
finally:
    gc.enable()
assert gc.isenabled()
print('Автоматический GC восстановлен:', gc.isenabled())
