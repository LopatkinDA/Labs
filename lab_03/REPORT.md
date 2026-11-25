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

Работа выполнена 25 ноября 2026 года в CPython 3.12.14, Windows 11, 64 бита. Использована только стандартная библиотека. Все пять файлов завершились с кодом 0, проверки assert пройдены. Для запуска следует перейти в каталог lab_03:

```text
python task_1.py
python task_2.py
python task_3.py
python task_4.py
python task_5.py
```

Программа task_2.py запрашивает число через input(). Для проверки введено 18. Встроенные min, max, sum, sorted и list.count не используются для реализации требуемых алгоритмов. sorted в задании 3 применяется только для стабильного представления множества имен в выводе.

### 2 Условия и классификация

В task_1.py обычные if/elif сначала проверяют диапазоны балла 0..100 и пропусков 0..5. При ошибке выводится сообщение, а блок else с классификацией не выполняется. Затем пороги проверяются по убыванию: 90, 75, 60; ветвь else соответствует 0..59. При пропусках больше трех отдельная цепочка if/elif заменяет уровень на предыдущий. Недостаточный уровень остается без изменений. match/case выбирает пояснение для exam, project, practice и неизвестного типа.

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

При выбранном порядке недостижимых ветвей нет: первая успешная проверка отсекает верхнюю часть диапазона, а следующие работают с оставшимися значениями. В каждой последующей ветви значения выше предыдущего порога уже недостижимы. Если поставить score >= 60 раньше score >= 90 в одной цепочке elif, высокий уровень окажется недостижимым. При ошибке диапазона блок else с классификацией пропускается — это предусмотренное поведение.

Обработаны десять записей из первых десяти сценариев. Получены готовые строки для каждой записи и сводка: недостаточный — 3, удовлетворительный — 2, хороший — 3, отличный — 2. Исходный список сравнен с копией и не изменен. Обработка одной записи требует O(1) времени и памяти, группы из n записей — O(n) времени; счетчики четырех категорий занимают O(1) дополнительной памяти, не считая входа и вывода.

### 3 Циклы и алгоритмические схемы

Для measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18] за первый проход вычислены сумма 144, минимум 7, максимум 21 и число четных 4. Среднее равно 14.4. Вторым проходом найдено 6 значений выше среднего: 15, 18, 18, 21, 15, 18. Результат сравнен с заранее заданным кортежем (144, 7, 21, 4, 14.4, 6).

Линейный поиск 18 вернул индекс 3 после четырех сравнений элементов с целью; поиск 99 вернул −1 после десяти сравнений. Индексы отсчитываются от нуля. Данный фрагмент работает с заданным непустым списком measurements; для пустого списка перед обращением к первому элементу потребовалась бы отдельная проверка.

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

Пересечение множеств сдавших lab_01 и lab_02 дало {anna, boris}. После добавления ('daria', 'lab_02', 4) появилась одна новая пара с результатом 4 и одной попыткой, обновились список Дарьи и множество сдавших lab_02. Полное перестроение не выполнялось; теперь обе работы сдавали все три студента.

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

Во вложенной функции marker находится в L, course из-за nonlocal — в E, len — в B после безуспешного поиска в L, E и G. В коде на уровне модуля course и outer находятся в G. Результат outer — ('Локальный курс: обновлен', 8), глобальное course сохранило «Основы программирования». В фабрике threshold принадлежит E, value — L возвращенной функции. Поля словарей и атрибуты объектов не являются самостоятельными уровнями LEGB.

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
| По студенту на 0,59,60,74,75,89,90,100 | 547/8; лидер 100 | 68.375; лидер 100 |

Для границ отдельно проверены категории: 0 и 59 — недостаточный; 60 и 74 — удовлетворительный; 75 и 89 — хороший; 90 и 100 — отличный. Дополнительно проверены минимум и максимум, форматирование пустых данных. Проверены шесть сценариев. Для основной группы дополнительно проверена неизменность входных данных.

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

В заданиях 1–3 код записан последовательными блоками без функций. В заданиях 4–5 оставлены функции, требуемые условием. Рейтинг формируется прямо в group_summary. Функции не изменяют входные коллекции. Считаем, что входные значения соответствуют контрактам: баллы — целые числа от 0 до 100. Названия name должны быть строками; повторяющиеся имена в словаре невозможны.

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
# Балл, тип работы, пропуски.
records = [
    (0, 'exam', 0),
    (59, 'project', 3),
    (60, 'practice', 0),
    (74, 'exam', 3),
    (75, 'project', 0),
    (89, 'practice', 3),
    (90, 'exam', 0),
    (100, 'project', 3),
    (90, 'exam', 4),
    (60, 'practice', 5),
]
before = records.copy()
counts = {'недостаточный': 0, 'удовлетворительный': 0,
          'хороший': 0, 'отличный': 0}

# Одна запись, десять записей группы и дополнительные проверки.
checks = [(90, 'exam', 0)]
checks += records
checks += [(-1, 'exam', 0), (101, 'exam', 0),
           (80, 'exam', -1), (80, 'exam', 6),
           (80, 'other', 0)]
expected = ['отличный',
 'недостаточный',
 'недостаточный',
 'удовлетворительный',
 'удовлетворительный',
 'хороший',
 'хороший',
 'отличный',
 'отличный',
 'хороший',
 'недостаточный',
 '',
 '',
 '',
 '',
 'хороший']
for i in range(len(checks)):
    score, work_type, absences = checks[i]
    print('Данные:', score, work_type, absences)
    if score < 0 or score > 100:
        print('Ошибка: балл должен быть от 0 до 100')
    elif absences < 0 or absences > 5:
        print('Ошибка: пропуски должны быть от 0 до 5')
    else:
        if score >= 90:
            level = 'отличный'
        elif score >= 75:
            level = 'хороший'
        elif score >= 60:
            level = 'удовлетворительный'
        else:
            level = 'недостаточный'
        if absences > 3:
            if level == 'отличный':
                level = 'хороший'
            elif level == 'хороший':
                level = 'удовлетворительный'
            elif level == 'удовлетворительный':
                level = 'недостаточный'
        match work_type:
            case 'exam':
                description = 'экзаменационная работа'
            case 'project':
                description = 'проектная работа'
            case 'practice':
                description = 'практическая работа'
            case _:
                description = 'неизвестный тип работы'
        print(description + '; уровень: ' + level)
        print('Ожидалось:', expected[i])
        assert level == expected[i]
        # В сводку входят только десять записей группы.
        if 1 <= i <= 10:
            counts[level] += 1
print('Сводка:', counts)
assert counts == {'недостаточный': 3, 'удовлетворительный': 2,
                  'хороший': 3, 'отличный': 2}

assert records == before
```

### task_2.py

```python
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
```

### task_3.py

```python
submissions = [
    ('anna', 'lab_01', 5),
    ('boris', 'lab_01', 4),
    ('anna', 'lab_02', 5),
    ('daria', 'lab_01', 3),
    ('boris', 'lab_02', 5),
    ('anna', 'lab_01', 4),
]
students = set()
labs = set()
by_student = {}
best = {}
attempts = {}
completed = {}

for student, lab, score in submissions:
    students.add(student)
    labs.add(lab)
    if student not in by_student:
        by_student[student] = []
    by_student[student].append((lab, score))
    key = (student, lab)
    if key not in best or score > best[key]:
        best[key] = score
    if key not in attempts:
        attempts[key] = 0
    attempts[key] += 1
    if lab not in completed:
        completed[lab] = set()
    completed[lab].add(student)

print('Студенты:', students)
print('Работы:', labs)
print('Попытки студентов:', by_student)
print('Лучшие результаты:', best)
print('Количество попыток:', attempts)
print('Обе работы:', completed['lab_01'] & completed['lab_02'])
assert best[('anna', 'lab_01')] == 5
assert attempts[('anna', 'lab_01')] == 2
assert completed['lab_01'] & completed['lab_02'] == {'anna', 'boris'}

# Добавляем одну запись, старые повторно не обрабатываем.
student, lab, score = 'daria', 'lab_02', 4
submissions.append((student, lab, score))
students.add(student)
labs.add(lab)
if student not in by_student:
    by_student[student] = []
by_student[student].append((lab, score))
key = (student, lab)
if key not in best or score > best[key]:
    best[key] = score
if key not in attempts:
    attempts[key] = 0
attempts[key] += 1
if lab not in completed:
    completed[lab] = set()
completed[lab].add(student)
print('После добавления:', by_student)
print('Теперь обе работы:', completed['lab_01'] & completed['lab_02'])
assert best[('daria', 'lab_02')] == 4
assert attempts[('daria', 'lab_02')] == 1

# Примеры запросов, включая ошибки.
commands = ['student anna', 'best anna lab_01', 'attempts boris lab_02',
            'completed lab_01', 'best nobody lab_99', 'delete anna', 'student', '']
for command in commands:
    print('Запрос:', command)
    parts = command.split()
    if len(parts) == 2 and parts[0] == 'student':
        if parts[1] in by_student:
            print(by_student[parts[1]])
        else:
            print('Нет данных')
    elif len(parts) == 3 and parts[0] == 'best':
        key = (parts[1], parts[2])
        if key in best:
            print(best[key])
        else:
            print('Нет данных')
    elif len(parts) == 3 and parts[0] == 'attempts':
        key = (parts[1], parts[2])
        if key in attempts:
            print(attempts[key])
        else:
            print('Нет данных')
    elif len(parts) == 2 and parts[0] == 'completed':
        if parts[1] in completed:
            print(sorted(completed[parts[1]]))
        else:
            print('Нет данных')
    else:
        print('Неизвестная команда или неверное число аргументов')
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
    rating = summaries.copy()
    for i in range(len(rating) - 1):
        for j in range(len(rating) - 1 - i):
            left = rating[j]['mean']
            right = rating[j + 1]['mean']
            if left is None:
                left = -1
            if right is None:
                right = -1
            if left < right:
                temporary = rating[j]
                rating[j] = rating[j + 1]
                rating[j + 1] = temporary
    return {
        'student_count': len(students),
        'result_count': count,
        'mean': average,
        'categories': categories,
        'leaders': find_top_students(students),
        'rating': rating,
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


original = deepcopy(students)
summaries = []
for name in students:
    summaries.append(student_summary(name, students[name]))
group = group_summary(students)
print(format_report(summaries, group))
assert students == original
assert group['mean'] == 1032 / 13
assert group['leaders'] == ['Дарья']

# Еще пять сценариев вместе с обычной группой дают шесть проверок.
one = group_summary({'А': [80]})
assert one['mean'] == 80
print('Один студент:', one['mean'], one['leaders'])

tied = group_summary({'А': [80, 100], 'Б': [90]})
assert tied['leaders'] == ['А', 'Б']
print('Два лидера:', tied['leaders'])

empty = group_summary({})
assert empty['mean'] is None
print('Пустая группа:', empty['mean'], empty['leaders'])

no_results = group_summary({'А': [], 'Б': [60]})
assert no_results['mean'] == 60
assert student_summary('А', [])['category'] == 'нет данных'
print('Студент без оценок:', no_results['mean'], no_results['leaders'])

boundaries = {'0': [0], '59': [59], '60': [60], '74': [74],
              '75': [75], '89': [89], '90': [90], '100': [100]}
border_group = group_summary(boundaries)
assert border_group['mean'] == 547 / 8
print('Границы:', border_group['mean'], border_group['leaders'])
for name in boundaries:
    print(name, classify(boundaries[name][0]))

assert minimum([]) is None
assert maximum([]) is None
assert mean([]) is None
```

