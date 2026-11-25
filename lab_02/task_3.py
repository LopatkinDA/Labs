import sys
import weakref

# Прогноз: счетчик будет 2, 3, 4, 3, 2.
data = [1, 2, 3]
print('После создания:', sys.getrefcount(data))
alias = data
print('После alias:', sys.getrefcount(data))
container = [data]
print('После контейнера:', sys.getrefcount(data))
del alias
print('После del alias:', sys.getrefcount(data))
container.clear()
print('После clear:', sys.getrefcount(data))

# Такой класс нужен, чтобы создать объект для слабой ссылки.
class Record:
    pass

# Прогноз: после del record слабая ссылка вернет None.
record = Record()
weak_record = weakref.ref(record)
print('До удаления:', weak_record())
del record
print('После удаления:', weak_record())

# Прогноз реестра: a, b, c -> a, b -> b.
a = Record()
b = Record()
c = Record()
registry = weakref.WeakValueDictionary()
registry['a'] = a
registry['b'] = b
registry['c'] = c
print('До удаления:', list(registry))
del c
print('После del c:', list(registry))
assert set(registry) == {'a', 'b'}
del a
print('После del a:', list(registry))
assert set(registry) == {'b'}
assert registry['b'] is b
