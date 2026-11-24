"""Имена, ссылки и независимые конфигурации."""
from copy import deepcopy


def main():
    print('Прогноз A: сначала один int; после += значения 11 и 10.')
    a = 10
    b = a
    print(a, b, id(a), id(b))
    a += 1
    print(a, b, id(a), id(b))
    assert (a, b) == (11, 10) and a is not b
    print('Прогноз B: append общий; после копирования изменения независимы.')
    first = [10, 20]
    second = first
    print(first, second, id(first), id(second))
    second.append(30)
    print(first, second, id(first), id(second))
    second = list(first)
    print('После переназначения: ==', first == second, 'is', first is second)
    second.append(40)
    print(first, second)
    assert first == [10, 20, 30] and second == [10, 20, 30, 40]
    print('Прогноз: присваивание разделяет весь словарь; deepcopy изолирует списки.')
    config = {'name': 'Учебный проект', 'members': ['Анна'],
              'launch': [['--port', '8000'], ['--debug', 'off']]}
    alias = config
    print('До:', config, alias)
    alias['members'].append('Борис')
    alias['launch'][0][1] = '9000'
    print('После общего изменения:', config, alias)
    independent = deepcopy(config)
    print('До независимого изменения:', config, independent)
    independent['members'].append('Дарья')
    independent['launch'][0][1] = '7000'
    print('После:', config, independent)
    assert alias is config
    assert independent is not config
    assert independent['members'] is not config['members']
    assert independent['launch'][0] is not config['launch'][0]
    assert config['members'] == ['Анна', 'Борис']
    assert config['launch'][0][1] == '9000'
    print('Итог: alias общий; independent и его изменяемые списки независимы.')


if __name__ == '__main__':
    main()
