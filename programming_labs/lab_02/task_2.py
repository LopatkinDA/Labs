"""Сравнение копий и вложенных списков."""
from copy import deepcopy


def main():
    original = [['Python', 5], ['Algorithms', 4]]
    alias = original
    shallow = original.copy()
    deep = deepcopy(original)

    def show(label):
        print(label)
        for name, obj in [('original', original), ('alias', alias),
                          ('shallow', shallow), ('deep', deep)]:
            print(name, obj, 'id:', id(obj), id(obj[0]), id(obj[0][1]))

    print('Прогноз: append виден у alias; вложенная правка также у shallow.')
    show('До изменений')
    original.append(['Databases', 5])
    show('После append')
    assert len(alias) == 3 and len(shallow) == len(deep) == 2
    original[0][1] = 3
    show('После изменения оценки')
    assert shallow[0][1] == 3 and deep[0][1] == 5
    assert alias is original and shallow[0] is original[0]
    assert deep[0] is not original[0]
    print('Прогноз матриц: три измененные строки против одной.')
    wrong_matrix = [[0] * 3] * 3
    correct_matrix = [[0] * 3 for _ in range(3)]
    wrong_matrix[0][0] = 1
    correct_matrix[0][0] = 1
    print('wrong:', wrong_matrix, [id(row) for row in wrong_matrix])
    print('correct:', correct_matrix, [id(row) for row in correct_matrix])
    assert wrong_matrix == [[1, 0, 0]] * 3
    assert correct_matrix == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert len({id(row) for row in correct_matrix}) == 3


if __name__ == '__main__':
    main()
