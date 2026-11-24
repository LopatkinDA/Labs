# Лабораторная работа № 3

Алгоритмы коллекции и функции

Выполнил:  
Группа:  
Проверил:  
Дата:  

## Цель работы

Реализовать условия, циклы, поиск, сортировку и обработку коллекций; выделить функции с явными контрактами и исследовать области видимости. Разработать анализатор учебных результатов и проверить его на обычных, граничных и пустых данных.

## Ход работы

### 1 Среда и запуск

Работа выполнена 24 ноября 2026 года в CPython 3.12.14, Windows 11, 64 бита. Использована только стандартная библиотека. Все пять файлов завершились с кодом 0, проверки assert пройдены. Для запуска следует перейти в каталог lab_03:

```text
python task_1.py
python task_2.py
python task_3.py
python task_4.py
python task_5.py
```

Программа task_2.py запрашивает число через input(). Для проверки введено 18. Встроенные min, max, sum, sorted и list.count не используются для реализации требуемых алгоритмов. sorted в задании 3 применяется только для стабильного представления множества имен в выводе.

### 2 Условия и классификация

В classify_record сначала проверяются диапазоны балла 0..100 и пропусков 0..5. При ошибке функция сразу возвращает сообщение и не выполняет классификацию. Затем пороги проверяются по убыванию: 90, 75, 60; ветвь else соответствует 0..59. При пропусках больше трех индекс уровня уменьшается, если он больше нуля. match/case выбирает пояснение для exam, project, practice и неизвестного типа.

Результаты сценариев приведены в таблице 1. Во всех строках ожидаемый результат совпал с фактическим; тип работы дополнительно определил соответствующее пояснение.

Таблица 1 — Проверка границ и дополнительных ветвей

| Балл | Тип | Пропуски | Ожидалось | Фактически |
| --- | --- | --- | --- | --- |
| 0 | exam | 0 | недостаточный | недостаточный |
| 59 | project | 3 | недостаточный | недостаточный |
| 60 | practice | 0 | удовлетворительный | удовлетворительный |
| 74 | exam | 3 | удовлетворительный | удовлетворительный |
| 75 | project | 0 | хороший | хороший |
| 89 | practice | 3 | хороший | хороший |
| 90 | exam | 0 | отличный | отличный |
| 100 | project | 3 | отличный | отличный |
| 90 | exam | 4 | хороший | хороший |
| 60 | practice | 5 | недостаточный | недостаточный |
| −1 и 101 | exam | 0 | ошибка балла | ошибка балла |
| 80 | exam | −1 и 6 | ошибка пропусков | ошибка пропусков |
| 80 | other | 0 | хороший; неизвестный тип | хороший; неизвестный тип |

При выбранном порядке недостижимых ветвей нет: первая успешная проверка отсекает верхнюю часть диапазона, а следующие работают с оставшимися значениями. В каждой последующей ветви значения выше предыдущего порога уже недостижимы. Если поставить score >= 60 раньше score >= 90 в одной цепочке elif, высокий уровень окажется недостижимым. После раннего возврата по ошибке классификация также недостижима — это предусмотренное поведение.

Обработаны десять записей из первых десяти сценариев. Получены готовые строки для каждой записи и сводка: недостаточный — 3, удовлетворительный — 2, хороший — 3, отличный — 2. Исходный список сравнен с копией и не изменен. Обработка одной записи требует O(1) времени и памяти, группы из n записей — O(n) времени; счетчики четырех категорий занимают O(1) дополнительной памяти, не считая входа и вывода.

### 3 Циклы и алгоритмические схемы

Для measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18] за первый проход вычислены сумма 144, минимум 7, максимум 21 и число четных 4. Среднее равно 14.4. Вторым проходом найдено 6 значений выше среднего: 15, 18, 18, 21, 15, 18. Результат сравнен с заранее заданным кортежем (144, 7, 21, 4, 14.4, 6).

Линейный поиск 18 вернул индекс 3 после четырех сравнений элементов с целью; поиск 99 вернул −1 после десяти сравнений. Индексы отсчитываются от нуля. Для пустого списка statistics возвращает None.

Псевдокод первого алгоритма:

```text
ЕСЛИ список пуст: вернуть отсутствие результата
сумма = 0; четные = 0
минимум = максимум = первый элемент
ДЛЯ каждого элемента:
    прибавить его к сумме
    при необходимости обновить минимум и максимум
    если элемент четный: увеличить счетчик
среднее = сумма / длина
выше = 0
ДЛЯ каждого элемента:
    если элемент > среднего: увеличить выше
вернуть вычисленные показатели
```

Проверка простоты перебирает делители d, пока d*d <= number. Для 0 и 1 получено False, 2 — True, 4 и 49 — False, 97 — True. Если составное число n = a*b, хотя бы один множитель не больше квадратного корня n: иначе произведение больше n. Поэтому делитель вне этого диапазона не может быть первым необходимым свидетельством составности.

Сортировка выбором создает копию списка, на каждом шаге ищет минимум неупорядоченного хвоста и меняет его местами с текущим элементом. Проверка [3, 1, 2, 1] дала [1, 1, 2, 3], исходник сохранен. Бинарный поиск работает только по отсортированной последовательности.

Псевдокод второго алгоритма:

```text
левая = 0; правая = длина - 1; сравнения = 0
ПОКА левая <= правая:
    середина = (левая + правая) // 2
    сравнения += 1
    ЕСЛИ элемент[середина] == цель:
        вернуть середину и сравнения
    сравнения += 1
    ЕСЛИ элемент[середина] < цель:
        левая = середина + 1
    ИНАЧЕ: правая = середина - 1
вернуть -1 и сравнения
```

В таблице 2 для обоих поисков использованы одни и те же списки 0..n−1, полученные собственной сортировкой обратного порядка. Считаются только сравнения значения элемента с целью: == и, если равенство ложно, <. Проверки границ цикла не считаются. Поэтому один шаг бинарного поиска может давать два сравнения.

Таблица 2 — Фактическое число сравнений

| n | Цель | Линейный | Бинарный |
| --- | --- | --- | --- |
| 10 | 0 | 1 | 5 |
| 10 | 5 | 6 | 5 |
| 10 | 9 | 10 | 7 |
| 10 | 10, нет в списке | 10 | 8 |
| 100 | 0 | 1 | 11 |
| 100 | 50 | 51 | 11 |
| 100 | 99 | 100 | 13 |
| 100 | 100, нет в списке | 100 | 14 |
| 1000 | 0 | 1 | 17 |
| 1000 | 500 | 501 | 17 |
| 1000 | 999 | 1000 | 19 |
| 1000 | 1000, нет в списке | 1000 | 20 |

На первом элементе линейный поиск выгоднее, но при удаленных целях и отсутствии элемента число сравнений растет линейно, у бинарного — логарифмически. Цена предварительной сортировки в счетчики поиска не включена; сортировка выбором делает n(n−1)/2 сравнений элементов, то есть 45, 4950 и 499500 для выбранных размеров. Для единственного запроса эта подготовка может быть дороже линейного поиска.

Таблица 3 — Сложность алгоритмов задания 2

| Алгоритм | Время в худшем случае | Дополнительная память |
| --- | --- | --- |
| Статистика в два прохода | O(n) | O(1) |
| Линейный поиск | O(n), лучший O(1) | O(1) |
| Проверка простоты числа m | O(√m) | O(1) |
| Сортировка выбором копии | O(n²) | O(n) для копии |
| Итеративный бинарный поиск | O(log n), лучший O(1) | O(1) |

Здесь n — длина списка, m — значение проверяемого числа. Оценки предполагают постоянную стоимость арифметики с числами рассматриваемого размера.

### 4 Коллекции и составные ключи

Из шести исходных записей получены студенты {anna, boris, daria} и работы {lab_01, lab_02}. Словарь by_student содержит: anna — [(lab_01, 5), (lab_02, 5), (lab_01, 4)]; boris — [(lab_01, 4), (lab_02, 5)]; daria — [(lab_01, 3)]. Лучшие результаты и число попыток приведены в таблице 4.

Таблица 4 — Результаты до добавления новой записи

| Ключ student, laboratory | Лучший результат | Попытки |
| --- | --- | --- |
| anna, lab_01 | 5 | 2 |
| anna, lab_02 | 5 | 1 |
| boris, lab_01 | 4 | 1 |
| boris, lab_02 | 5 | 1 |
| daria, lab_01 | 3 | 1 |

Пересечение множеств сдавших lab_01 и lab_02 дало {anna, boris}. После add(index, ('daria', 'lab_02', 4)) появилась одна новая пара с результатом 4 и одной попыткой, обновились список Дарьи и множество сдавших lab_02. Полное перестроение не выполнялось; теперь обе работы сдавали все три студента.

Множество хранит уникальные хешируемые значения. Составной ключ из двух строк хешируем, потому что кортеж неизменяем и его элементы хешируемы. Не любой кортеж является допустимым ключом: наличие списка внутри делает его нехешируемым. Список сам изменяем и не имеет подходящего хеша, поэтому ключом быть не может. Словарь дает прямой поиск по паре, тогда как список записей пришлось бы просматривать.

Таблица 5 — Средняя сложность операций коллекций

| Структура | Добавление | Поиск | Примечание |
| --- | --- | --- | --- |
| list | append O(1) амортизированно | O(n) по значению | Индексация O(1) |
| tuple | Изменение запрещено | O(n) по значению | Создание нового O(n) |
| set | O(1) в среднем | O(1) в среднем | При плохих коллизиях O(n) |
| dict | O(1) в среднем | O(1) в среднем | При плохих коллизиях O(n) |

Для фиксированной длины имен одно добавление в индексы занимает O(1) в среднем, построение по n попыткам — O(n) времени и O(n) памяти. Пересечение двух множеств требует в среднем O(min(a, b)) проверок принадлежности и памяти под результат. Разбор команды занимает O(L), где L — длина строки. Формирование ответа student требует O(k) по числу попыток; completed дополнительно сортирует s имен за O(s log s).

Таблица 6 — Запросы и фактические ответы

| Запрос | Ответ |
| --- | --- |
| student anna | [('lab_01', 5), ('lab_02', 5), ('lab_01', 4)] |
| best anna lab_01 | 5 |
| attempts boris lab_02 | 1 |
| completed lab_01 | ['anna', 'boris', 'daria'] |
| best nobody lab_99 | Нет данных |
| delete anna | Неизвестная команда или неверное число аргументов |
| student без аргумента и пустая строка | Сообщение об ошибке команды, без исключения |

### 5 Функции параметры и области видимости

arithmetic_mean вычисляет среднее непустого списка; пустой список вызывает ValueError. normalize_name объединяет части одним пробелом и делает первую букву каждой части прописной. Для пустого имени предусмотрен ранний return ''. build_report имеет только именованные параметры precision и prefix; при пустых результатах рано возвращает строку «нет данных». collect_tags удаляет пустые и повторные теги, сохраняя порядок первых вхождений. Для этого используется обычный цикл и проверка tag not in result. Для n тегов такая проверка требует O(n²) времени в худшем случае и O(n) памяти результата.

Таблица 7 — Минимум три проверки каждой функции

| Функция | Входы | Ожидалось и получено |
| --- | --- | --- |
| arithmetic_mean | [1,3]; [5]; [−2,2] | 2.0; 5.0; 0.0 |
| normalize_name | пробелы и «иВАН иВАНОВ»; ''; « АННА » | «Иван Иванов»; ''; «Анна» |
| build_report | Анна [80,90]; Борис []; Дарья [91], precision=0 | 85.00; нет данных; 91 |
| collect_tags | Python, python, пусто, IT; A,a без lower; без аргументов | ('python','it'); ('A','a'); () |

Дополнительно проверен ValueError для среднего пустого списка. Показаны позиционный вызов build_report('анна', [80, 90]), именованный build_report(student='дарья', results=[91], precision=0) и распаковка build_report(*arguments, **options). Последний вызов дал «Итог: Анна — 85.0». Исходные результаты [80, 90] сохранены.

Рисунок 1 соответствует outer и inner из task_4.py. nonlocal course меняет привязку во внешней функции, не глобальную переменную.

```text
L  inner: marker = 'обновлен'
   course объявлен nonlocal
          |
E  outer: course = 'Локальный курс'
          после inner: 'Локальный курс: обновлен'
          |
G  module: course = 'Основы программирования'
   outer, arithmetic_mean и остальные функции
          |
B  builtins: len, print, ValueError и другие
```

Рисунок 1 — Области видимости LEGB

Во вложенной функции marker находится в L, course из-за nonlocal — в E, len — в B после безуспешного поиска в L, E и G. В main имя course находится в G; outer также находится в G. Результат outer — ('Локальный курс: обновлен', 8), глобальное course сохранило «Основы программирования». В фабрике threshold принадлежит E, value — L возвращенной функции. Поля словарей и атрибуты объектов не являются самостоятельными уровнями LEGB.

У ошибочной функции bad_add_result список по умолчанию создается один раз при выполнении def. Поэтому вызовы с 1 и 2 вернули один объект [1, 2]. В исправленной функции по умолчанию None, а результат создается заново: [1] и [2]. Явно переданный список также не изменяется, поскольку сначала выполняется results.copy(), а затем append(value) для копии. Это требует O(n) времени и памяти; у ошибочного append было амортизированное O(1), но неверный жизненный цикл состояния.

apply_to_results(double, [1,2,3]) вернула [2,4,6], а с lambda x: x+5 — [6,7,8]. Обработка n значений требует O(n) времени при O(1) стоимости операции и O(n) памяти результата. Два замыкания make_threshold_checker(60) и make_threshold_checker(90) независимо сохраняют свои threshold; для 75 получены True и False, пороги включаются. Создание и один вызов проверки требуют O(1).

### 6 Анализатор учебных результатов

Программа разделена на вычисление числовых показателей, классификацию, сводки, рейтинг и форматирование. Политика пустых данных: среднее, минимум и максимум равны None; категория «нет данных»; студент остается в сводке и в конце рейтинга, но не участвует в выборе лидеров и знаменателе общего среднего. Пустая группа дает среднее None и пустой список лидеров.

Общее среднее определяется по всем оценкам с одинаковым весом каждой оценки: 1032 / 13 = 79.38461538461539. Это определение необходимо, поскольку у студентов разное количество результатов. Для вывода число округляется до 79.38; сравнение лидеров выполняется до округления.

Таблица 8 — Фактическая индивидуальная статистика

| Студент | Среднее | Минимум | Максимум | Категория |
| --- | --- | --- | --- | --- |
| Анна | 85.25 | 78 | 91 | хороший |
| Борис | 66.67 | 60 | 72 | удовлетворительный |
| Дарья | 93.75 | 90 | 97 | отличный |
| Илья | 58.00 | 55 | 61 | недостаточный |

Лидер — Дарья. Рейтинг: Дарья, Анна, Борис, Илья. В каждой из четырех категорий по одному студенту, без данных — 0. Рейтинг строится простой пузырьковой сортировкой по копии списка сводок, поэтому исходный словарь и списки оценок сохранены. Равные средние сохраняют порядок входа. Лидеры определяются по точному равенству вычисленных средних; для произвольных приближенных вещественных измерений понадобилось бы отдельно определить допуск.

Таблица 9 — Проверки интеграционного задания

| Сценарий | Ожидалось | Фактически |
| --- | --- | --- |
| Исходная группа | 1032/13; лидер Дарья | 79.38461538461539; Дарья |
| Один студент А: [80] | 80; А | 80.0; А |
| А: [80,100], Б: [90] | 90; два лидера А, Б | 90.0; А, Б |
| Пустая группа | None; [] | None; [] |
| А: [], Б: [60] | 60; Б; А без данных | 60.0; Б; А без данных |
| А: [] | None; [] | None; [] |
| По студенту на 0,59,60,74,75,89,90,100 | 547/8; лидер 100 | 68.375; лидер 100 |

Для границ отдельно проверены категории: 0 и 59 — недостаточный; 60 и 74 — удовлетворительный; 75 и 89 — хороший; 90 и 100 — отличный. Дополнительно проверены минимум и максимум, форматирование пустых данных. Во всех семи групповых сценариях подтверждена неизменность входных данных.

Таблица 10 — Контракты публичных функций

| Функция | Допустимый вход | Результат и особые случаи |
| --- | --- | --- |
| mean(values) | Список конечных чисел | Среднее float; [] → None |
| minimum(values) | Список конечных чисел | Наименьшее значение; [] → None |
| maximum(values) | Список конечных чисел | Наибольшее значение; [] → None |
| classify(score) | Конечное число 0..100 или None | Категория; None → «нет данных». Балл должен быть в диапазоне 0..100 |
| student_summary(name, results) | Имя str, список целых баллов 0..100 | Новый dict с name, count, mean, minimum, maximum, category; пустой список допустим |
| group_summary(students) | dict имен и допустимых списков баллов | Числа студентов и оценок, общее среднее, категории, лидеры, рейтинг; пустые данные допустимы |
| find_top_students(students) | Тот же dict | Список всех имен с максимальным средним; пусто или все без данных → [] |
| format_report(student_data, group_data) | Список сводок и словарь group_summary | Строка отчета; None заменяется словами; вход не меняется |
| rank(summaries) | Список корректных словарей student_summary | Новый список по убыванию среднего; None в конце; равные стабильны |

Функции не изменяют входные коллекции. Считаем, что входные значения соответствуют контрактам: баллы — целые числа от 0 до 100. Названия name должны быть строками; повторяющиеся имена в словаре невозможны.

Пусть S — число студентов, M — общее число оценок. mean, minimum и maximum требуют O(k) времени для списка длины k и O(1) дополнительной памяти. student_summary выполняет несколько линейных проходов, но остается O(k) и создает сводку постоянного размера. find_top_students требует O(M+S) времени и до O(S) памяти для всех лидеров. Сбор числовой статистики группы имеет O(M+S), пузырьковая сортировка рейтинга — O(S²) в худшем случае. Поэтому group_summary в данной реализации требует O(M+S²) времени и O(S) дополнительной памяти. format_report линеен по объему формируемого текста и хранит этот текст в памяти. Повторные проходы при построении сводок и поиске лидеров не меняют порядок роста, но увеличивают постоянный коэффициент.

## Вывод

Ранние проверки диапазонов исключили неверную классификацию, а обработка границ выявила все переходы между уровнями. Сравнение поисков показало линейный и логарифмический рост числа сравнений, при этом сортировка требует отдельной подготовки. Словари и множества упростили обновление результатов и запросы по составным ключам. Декомпозиция отделила вычисления от вывода, позволила задать политику пустых данных и проверить функции независимо. Исследование LEGB и значений по умолчанию показало, как избежать скрытого изменения общего состояния.

## Источники

1. [Задание лабораторной работы 3](https://github.com/itmo-faculty-applied-informatics/fai_topit_fundamentals_of_programming/blob/main/labs/lab_03_algorithms_collections_functions.md).
2. [Требования ИТМО к оформлению — раздел 4](https://student.itmo.ru/files/1314). Использованы как ориентир оформления учебного отчета.
3. [Руководство по оформлению Markdown](https://gist.github.com/Jekins/2bf2d0638163f1294637).



## Приложение Исходный код

### task_1.py

```python
"""Условия, match и обработка группы записей."""
LEVELS = ('недостаточный', 'удовлетворительный', 'хороший', 'отличный')


def classify_record(score: int, work_type: str, absences: int) -> tuple[str, str]:
    """Возвращает уровень и пояснение; ошибка диапазона прекращает классификацию."""
    if not 0 <= score <= 100:
        return '', 'Ошибка: результат вне диапазона 0..100'
    elif not 0 <= absences <= 5:
        return '', 'Ошибка: пропуски вне диапазона 0..5'
    else:
        if score >= 90:
            index = 3
        elif score >= 75:
            index = 2
        elif score >= 60:
            index = 1
        else:
            index = 0
    if absences > 3 and index > 0:
        index -= 1
    match work_type:
        case 'exam':
            description = 'экзаменационная работа'
        case 'project':
            description = 'проектная работа'
        case 'practice':
            description = 'практическая работа'
        case _:
            description = 'неизвестный тип работы'
    return LEVELS[index], description


def main():
    cases = [(0, 'exam', 0, LEVELS[0]), (59, 'project', 3, LEVELS[0]),
             (60, 'practice', 0, LEVELS[1]), (74, 'exam', 3, LEVELS[1]),
             (75, 'project', 0, LEVELS[2]), (89, 'practice', 3, LEVELS[2]),
             (90, 'exam', 0, LEVELS[3]), (100, 'project', 3, LEVELS[3]),
             (90, 'exam', 4, LEVELS[2]), (60, 'practice', 5, LEVELS[0]),
             (-1, 'exam', 0, ''), (101, 'exam', 0, ''),
             (80, 'exam', -1, ''), (80, 'exam', 6, ''),
             (80, 'other', 0, LEVELS[2])]
    for score, kind, absences, expected in cases:
        actual, description = classify_record(score, kind, absences)
        assert actual == expected
        print((score, kind, absences), 'ожидалось:', expected,
              'получено:', actual, description)
    records = []
    for score, kind, absences, expected in cases[:10]:
        records.append((score, kind, absences))
    before = records.copy()
    counts = {}
    for level in LEVELS:
        counts[level] = 0
    for score, kind, absences in records:
        level, description = classify_record(score, kind, absences)
        counts[level] += 1
        print(score, kind, absences, ':', description, '; уровень', level)
    assert records == before
    assert counts == {LEVELS[0]: 3, LEVELS[1]: 2, LEVELS[2]: 3, LEVELS[3]: 2}
    print('Сводка:', counts)
    print('Проверки задания 1 пройдены')


if __name__ == '__main__':
    main()
```

### task_2.py

```python
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
```

### task_3.py

```python
"""Индексы результатов и безопасный разбор запросов."""
SUBMISSIONS = [('anna', 'lab_01', 5), ('boris', 'lab_01', 4),
               ('anna', 'lab_02', 5), ('daria', 'lab_01', 3),
               ('boris', 'lab_02', 5), ('anna', 'lab_01', 4)]


def empty_index():
    return {'students': set(), 'labs': set(), 'by_student': {},
            'best': {}, 'attempts': {}, 'completed': {}}


def add(index, record):
    student, lab, score = record
    key = student, lab
    index['students'].add(student)
    index['labs'].add(lab)
    if student not in index['by_student']:
        index['by_student'][student] = []
    index['by_student'][student].append((lab, score))
    if key not in index['best'] or score > index['best'][key]:
        index['best'][key] = score
    if key not in index['attempts']:
        index['attempts'][key] = 0
    index['attempts'][key] += 1
    if lab not in index['completed']:
        index['completed'][lab] = set()
    index['completed'][lab].add(student)


def query(index, command):
    parts = command.split()
    if len(parts) == 2 and parts[0] == 'student':
        name = parts[1]
        if name in index['by_student']:
            return str(index['by_student'][name])
        return 'Нет данных'
    elif len(parts) == 3 and parts[0] == 'best':
        key = (parts[1], parts[2])
        if key in index['best']:
            return str(index['best'][key])
        return 'Нет данных'
    elif len(parts) == 3 and parts[0] == 'attempts':
        key = (parts[1], parts[2])
        if key in index['attempts']:
            return str(index['attempts'][key])
        return 'Нет данных'
    elif len(parts) == 2 and parts[0] == 'completed':
        lab = parts[1]
        if lab in index['completed']:
            return str(sorted(index['completed'][lab]))
        return 'Нет данных'
    return 'Неизвестная команда или неверное число аргументов'


def main():
    index = empty_index()
    for record in SUBMISSIONS:
        add(index, record)
    print('Индексы до добавления:', index)
    both = index['completed']['lab_01'] & index['completed']['lab_02']
    print('Обе работы:', sorted(both))
    assert both == {'anna', 'boris'}
    assert index['best'][('anna', 'lab_01')] == 5
    assert index['attempts'][('anna', 'lab_01')] == 2
    add(index, ('daria', 'lab_02', 4))
    print('После добавления daria lab_02 4:', index)
    assert index['attempts'][('daria', 'lab_02')] == 1
    for command in ('student anna', 'best anna lab_01', 'attempts boris lab_02',
                    'completed lab_01', 'best nobody lab_99', 'delete anna',
                    'student', ''):
        print(command, '=>', query(index, command))
    assert query(index, 'best anna lab_01') == '5'
    assert query(index, 'best nobody lab_99') == 'Нет данных'
    assert query(index, 'student').startswith('Неизвестная')
    print('Проверки задания 3 пройдены')


if __name__ == '__main__':
    main()
```

### task_4.py

```python
"""Контракты, параметры, LEGB и замыкания."""


def arithmetic_mean(values: list[float]) -> float:
    """Среднее непустого списка; пустой список вызывает ValueError."""
    if not values:
        raise ValueError('Пустой список')
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def normalize_name(name: str) -> str:
    """Убирает лишние пробелы; части имени записывает с прописной буквы."""
    if not name.strip():
        return ''
    parts = name.split()
    result = []
    for part in parts:
        result.append(part.capitalize())
    return ' '.join(result)


def build_report(student: str, results: list[int], *, precision: int = 2,
                 prefix: str = 'Результат') -> str:
    """Отчет о среднем; пустые результаты обозначаются словами «нет данных»."""
    if precision < 0:
        raise ValueError('precision должен быть неотрицательным')
    if not results:
        return f'{prefix}: {normalize_name(student)} — нет данных'
    return f'{prefix}: {normalize_name(student)} — {arithmetic_mean(results):.{precision}f}'


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Очищает теги и сохраняет порядок первых вхождений."""
    result = []
    for tag in tags:
        tag = tag.strip()
        if lowercase:
            tag = tag.lower()
        if tag != '' and tag not in result:
            result.append(tag)
    return tuple(result)


course = 'Основы программирования'


def outer():
    course = 'Локальный курс'

    def inner():
        nonlocal course
        marker = 'обновлен'
        course = course + ': ' + marker
        return course, len(marker)

    return inner()


def bad_add_result(value, results=[]):
    results.append(value)
    return results


def add_result(value, results=None):
    if results is None:
        results = []
    # Копирование также защищает явно переданный список от изменения.
    new_results = results.copy()
    new_results.append(value)
    return new_results


def apply_to_results(operation, values):
    result = []
    for value in values:
        result.append(operation(value))
    return result


def make_threshold_checker(threshold):
    def check(value):
        return value >= threshold
    return check


def double(value):
    return value * 2


def main():
    assert arithmetic_mean([1.0, 3.0]) == 2.0
    assert arithmetic_mean([5.0]) == 5.0
    assert arithmetic_mean([-2.0, 2.0]) == 0.0
    try:
        arithmetic_mean([])
    except ValueError:
        pass
    else:
        raise AssertionError('Ожидался ValueError')
    assert normalize_name('  иВАН   иВАНОВ ') == 'Иван Иванов'
    assert normalize_name('') == ''
    assert normalize_name(' АННА ') == 'Анна'
    assert build_report('анна', [80, 90]) == 'Результат: Анна — 85.00'
    assert build_report('борис', [], prefix='Итог') == 'Итог: Борис — нет данных'
    assert build_report(student='дарья', results=[91], precision=0) == 'Результат: Дарья — 91'
    assert collect_tags(' Python ', 'python', '', 'IT') == ('python', 'it')
    assert collect_tags('A', 'a', lowercase=False) == ('A', 'a')
    assert collect_tags() == ()
    values = [80, 90]
    before = values.copy()
    arguments = ['анна', values]
    options = {'precision': 1, 'prefix': 'Итог'}
    print(build_report(*arguments, **options))
    assert values == before
    print('Теги:', collect_tags(' Python ', 'python', ' IT '))
    print('LEGB:', outer(), 'global:', course)
    assert course == 'Основы программирования'
    first = bad_add_result(1)
    second = bad_add_result(2)
    assert first is second and first == [1, 2]
    print('Общий default:', first, second)
    assert add_result(1) == [1] and add_result(2) == [2]
    assert add_result(3, values) == [80, 90, 3] and values == before
    print('Исправлено:', add_result(1), add_result(2))
    print('Именованная функция:', apply_to_results(double, [1, 2, 3]))
    print('lambda:', apply_to_results(lambda x: x + 5, [1, 2, 3]))
    assert apply_to_results(double, [1, 2]) == [2, 4]
    assert apply_to_results(lambda x: x + 5, [1, 2]) == [6, 7]
    check60 = make_threshold_checker(60)
    check90 = make_threshold_checker(90)
    assert check60(75) and not check90(75)
    assert check60(60) and check90(90)
    print('Пороги 60 и 90 для 75:', check60(75), check90(75))
    print('Проверки задания 4 пройдены')


if __name__ == '__main__':
    main()
```

### task_5.py

```python
"""Простой анализатор результатов студентов."""
from copy import deepcopy

students = {
    'Анна': [78, 91, 84, 88],
    'Борис': [60, 72, 68],
    'Дарья': [95, 93, 97, 90],
    'Илья': [55, 61],
}


def mean(values):
    """Среднее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    total = 0
    for value in values:
        total += value
    return total / len(values)


def minimum(values):
    """Наименьшее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values):
    """Наибольшее значение. Для пустого списка возвращаем None."""
    if len(values) == 0:
        return None
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def classify(score):
    """Определяем категорию среднего балла от 0 до 100."""
    if score is None:
        return 'нет данных'
    if score >= 90:
        return 'отличный'
    elif score >= 75:
        return 'хороший'
    elif score >= 60:
        return 'удовлетворительный'
    else:
        return 'недостаточный'


def student_summary(name, results):
    """Собираем показатели одного студента в словарь."""
    average = mean(results)
    return {
        'name': name,
        'count': len(results),
        'mean': average,
        'minimum': minimum(results),
        'maximum': maximum(results),
        'category': classify(average),
    }


def rank(summaries):
    """Сортируем копию списка сводок по убыванию среднего балла."""
    result = summaries.copy()
    # Пузырьковая сортировка: сравниваем соседние записи.
    for i in range(len(result) - 1):
        for j in range(len(result) - 1 - i):
            left = result[j]['mean']
            right = result[j + 1]['mean']
            # Студенты без оценок должны попасть в конец.
            if left is None:
                left = -1
            if right is None:
                right = -1
            if left < right:
                temporary = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temporary
    return result


def find_top_students(students):
    """Находим всех студентов с самым высоким средним баллом."""
    best = None
    leaders = []
    for name in students:
        average = mean(students[name])
        if average is None:
            continue
        if best is None or average > best:
            best = average
            leaders = [name]
        elif average == best:
            leaders.append(name)
    return leaders


def group_summary(students):
    """Собираем общую статистику, лидеров и рейтинг группы."""
    summaries = []
    categories = {
        'недостаточный': 0,
        'удовлетворительный': 0,
        'хороший': 0,
        'отличный': 0,
        'нет данных': 0,
    }
    total = 0
    count = 0
    for name in students:
        values = students[name]
        summary = student_summary(name, values)
        summaries.append(summary)
        categories[summary['category']] += 1
        for value in values:
            total += value
            count += 1
    if count == 0:
        average = None
    else:
        average = total / count
    return {
        'student_count': len(students),
        'result_count': count,
        'mean': average,
        'categories': categories,
        'leaders': find_top_students(students),
        'rating': rank(summaries),
    }


def format_report(student_data, group_data):
    """Формируем текст из готовых сводок."""
    lines = []
    for row in student_data:
        if row['mean'] is None:
            line = row['name'] + ': нет данных'
        else:
            average = round(row['mean'], 2)
            line = f"{row['name']}: среднее {average}; "
            line += f"min {row['minimum']}; max {row['maximum']}; "
            line += row['category']
        lines.append(line)
    if group_data['mean'] is None:
        lines.append('Среднее группы: нет данных')
    else:
        average = round(group_data['mean'], 2)
        lines.append('Среднее группы: ' + str(average))
    if len(group_data['leaders']) == 0:
        lines.append('Лидеры: нет')
    else:
        lines.append('Лидеры: ' + ', '.join(group_data['leaders']))
    lines.append('Категории: ' + str(group_data['categories']))
    names = []
    for row in group_data['rating']:
        names.append(row['name'])
    lines.append('Рейтинг: ' + ', '.join(names))
    return '\n'.join(lines)


def main():
    original = deepcopy(students)
    summaries = []
    for name in students:
        summaries.append(student_summary(name, students[name]))
    group = group_summary(students)
    print(format_report(summaries, group))
    assert students == original
    assert group['mean'] == 1032 / 13
    assert group['leaders'] == ['Дарья']

    # Название сценария, данные, ожидаемое среднее, ожидаемые лидеры.
    boundaries = {
        '0': [0], '59': [59], '60': [60], '74': [74],
        '75': [75], '89': [89], '90': [90], '100': [100],
    }
    checks = [
        ('обычная группа', students, 1032 / 13, ['Дарья']),
        ('один студент', {'А': [80]}, 80, ['А']),
        ('равные лидеры', {'А': [80, 100], 'Б': [90]}, 90, ['А', 'Б']),
        ('пустая группа', {}, None, []),
        ('нет результатов', {'А': [], 'Б': [60]}, 60, ['Б']),
        ('все без результатов', {'А': []}, None, []),
        ('границы', boundaries, 547 / 8, ['100']),
    ]
    for label, data, expected_mean, expected_leaders in checks:
        before = deepcopy(data)
        actual = group_summary(data)
        assert actual['mean'] == expected_mean
        assert actual['leaders'] == expected_leaders
        assert data == before
        print(label, '=>', actual['mean'], actual['leaders'], 'OK')

    category_checks = [
        (0, 'недостаточный'), (59, 'недостаточный'),
        (60, 'удовлетворительный'), (74, 'удовлетворительный'),
        (75, 'хороший'), (89, 'хороший'),
        (90, 'отличный'), (100, 'отличный'),
    ]
    for score, expected in category_checks:
        assert classify(score) == expected
    assert mean([]) is None
    assert minimum([]) is None
    assert maximum([]) is None
    assert minimum([2, -1, 4]) == -1
    assert maximum([2, -1, 4]) == 4
    assert mean([2, 4]) == 3
    assert student_summary('А', [])['category'] == 'нет данных'
    names = []
    for row in group['rating']:
        names.append(row['name'])
    assert names == ['Дарья', 'Анна', 'Борис', 'Илья']
    empty_student_group = group_summary({'А': [], 'Б': [60]})
    assert empty_student_group['rating'][0]['name'] == 'Б'
    assert empty_student_group['rating'][1]['name'] == 'А'
    tied_group = group_summary({'А': [90], 'Б': [90]})
    assert tied_group['rating'][0]['name'] == 'А'
    assert tied_group['rating'][1]['name'] == 'Б'
    empty_report = format_report(
        [student_summary('А', [])], group_summary({'А': []})
    )
    assert 'нет данных' in empty_report
    print('Проверки задания 5 пройдены')


if __name__ == '__main__':
    main()
```

