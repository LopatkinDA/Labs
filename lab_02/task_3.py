"""Сильные и слабые ссылки."""
import sys
import weakref


class Record:
    pass


def main():
    print('Прогноз счетчика: +1 alias, +1 контейнер, -1 del, -1 clear.')
    data = [1, 2, 3]
    counts = [sys.getrefcount(data)]
    alias = data
    counts.append(sys.getrefcount(data))
    container = [data]
    counts.append(sys.getrefcount(data))
    del alias
    counts.append(sys.getrefcount(data))
    container.clear()
    counts.append(sys.getrefcount(data))
    print('Счетчики:', counts)
    assert counts[1] == counts[0] + 1
    assert counts[2] == counts[0] + 2
    assert counts[3] == counts[0] + 1
    assert counts[4] == counts[0]
    print('Прогноз weakref: после удаления последней сильной ссылки None.')
    record = Record()
    weak_record = weakref.ref(record)
    print('До del:', weak_record())
    del record
    print('После del:', weak_record())
    assert weak_record() is None
    print('Прогноз реестра: a,b,c -> a,b -> b.')
    a = Record()
    b = Record()
    temporary = Record()
    registry = weakref.WeakValueDictionary()
    registry['a'] = a
    registry['b'] = b
    registry['c'] = temporary
    print('До:', sorted(registry.keys()))
    del temporary
    print('После del temporary:', sorted(registry.keys()))
    assert set(registry) == {'a', 'b'}
    del a
    print('После del a:', sorted(registry.keys()))
    assert set(registry) == {'b'} and registry['b'] is b


if __name__ == '__main__':
    main()
