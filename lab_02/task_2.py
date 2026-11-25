import copy

original = [['Python', 5], ['Algorithms', 4]]
alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

print('Прогноз: append изменит original и alias.')
print('Замена оценки изменит еще и shallow. deep не изменится.')


print('До изменений')
print('original:', original)
print('id списка, строки, оценки:', id(original), id(original[0]), id(original[0][1]))
print('alias:', alias)
print('id списка, строки, оценки:', id(alias), id(alias[0]), id(alias[0][1]))
print('shallow:', shallow)
print('id списка, строки, оценки:', id(shallow), id(shallow[0]), id(shallow[0][1]))
print('deep:', deep)
print('id списка, строки, оценки:', id(deep), id(deep[0]), id(deep[0][1]))

original.append(['Databases', 5])
print('После append')
print('original:', original)
print('id списка, строки, оценки:', id(original), id(original[0]), id(original[0][1]))
print('alias:', alias)
print('id списка, строки, оценки:', id(alias), id(alias[0]), id(alias[0][1]))
print('shallow:', shallow)
print('id списка, строки, оценки:', id(shallow), id(shallow[0]), id(shallow[0][1]))
print('deep:', deep)
print('id списка, строки, оценки:', id(deep), id(deep[0]), id(deep[0][1]))

original[0][1] = 3
print('После замены оценки')
print('original:', original)
print('id списка, строки, оценки:', id(original), id(original[0]), id(original[0][1]))
print('alias:', alias)
print('id списка, строки, оценки:', id(alias), id(alias[0]), id(alias[0][1]))
print('shallow:', shallow)
print('id списка, строки, оценки:', id(shallow), id(shallow[0]), id(shallow[0][1]))
print('deep:', deep)
print('id списка, строки, оценки:', id(deep), id(deep[0]), id(deep[0][1]))

print('Прогноз: в wrong_matrix изменятся все строки, в correct_matrix — одна.')
wrong_matrix = [[0] * 3] * 3
correct_matrix = [[0] * 3 for _ in range(3)]
wrong_matrix[0][0] = 1
correct_matrix[0][0] = 1
print('Неправильно:', wrong_matrix)
print('Правильно:', correct_matrix)
print('id строк неправильной матрицы:')
for row in wrong_matrix:
    print(id(row))
print('id строк правильной матрицы:')
for row in correct_matrix:
    print(id(row))
