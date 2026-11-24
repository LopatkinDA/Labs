"""CLI только разбирает команды и вызывает сервисные методы."""
import logging
import shlex
import tracemalloc
from pathlib import Path
from .models import Student, Laboratory
from .exceptions import CourseTrackerError, ValidationError
from .storage import load_course, save_course, import_csv, export_csv
from .memory import memory_report, profile_reports

HELP = '''help | exit | save
student add ID "Имя Фамилия" Группа
student list [name|group|id] | student show ID
student activate ID | student deactivate ID | student search текст
lab add ID "Название" максимум ГГГГ-ММ-ДД теги[,теги] ["Описание"]
lab list | lab show ID | lab search текст
submit студент работа балл ["Комментарий"]
submission accept студент работа номер
submission reject студент работа номер ["Причина"]
history студент
report student ID | report group | report lab ID | report missing
top [число]
import students путь.csv | import submissions путь.csv
export json путь.json | export csv путь.csv
snapshot create | snapshot restore | undo
memory | memory profile
Пример: student add s001 "Анна Смирнова" P3120'''


def student_command(course, args):
    if not args:
        raise ValidationError('Укажите действие student. Введите help.')
    if args[0] == 'add' and len(args) == 4:
        course.add_student(Student(args[1], args[2], args[3]))
        return 'Студент добавлен.'
    if args[0] == 'list' and len(args) in (1, 2):
        sort_by = args[1] if len(args) == 2 else 'name'
        return course.list_students(sort_by)
    if args[0] == 'show' and len(args) == 2:
        return course.get_student(args[1])
    if args[0] in ('activate', 'deactivate') and len(args) == 2:
        course.set_active(args[1], args[0] == 'activate')
        return 'Статус студента изменен.'
    if args[0] == 'search' and len(args) >= 2:
        return course.search_students(' '.join(args[1:]))
    raise ValidationError('Неверная команда student. Введите help.')


def lab_command(course, args):
    if not args:
        raise ValidationError('Укажите действие lab. Введите help.')
    if args[0] == 'add' and len(args) in (6, 7):
        description = args[6] if len(args) == 7 else ''
        lab = Laboratory(args[1], args[2], float(args[3]), args[4],
                         set(args[5].split(',')), description)
        course.add_lab(lab)
        return 'Лабораторная добавлена.'
    if args[0] == 'list' and len(args) == 1:
        return list(course.laboratories.values())
    if args[0] == 'show' and len(args) == 2:
        return course.get_lab(args[1])
    if args[0] == 'search' and len(args) >= 2:
        return course.search_labs(' '.join(args[1:]))
    raise ValidationError('Неверная команда lab. Введите help.')


def report_command(course, args):
    if args == ['group']:
        return course.group_summary()
    if len(args) == 2 and args[0] == 'student':
        return course.student_summary(args[1])
    if len(args) == 2 and args[0] == 'lab':
        return course.lab_summary(args[1])
    if args == ['missing']:
        missing = {}
        for row in course.report_rows():
            missing[row['student_id']] = row['missing']
        return missing
    raise ValidationError('Неверная команда report. Введите help.')


def execute(course, parts, state_path):
    """Выбираем действие через match; вычисления остаются в сервисном слое."""
    command = parts[0]
    args = parts[1:]
    match command:
        case 'help':
            if args:
                raise ValidationError('help не принимает аргументы')
            return HELP
        case 'student':
            return student_command(course, args)
        case 'lab':
            return lab_command(course, args)
        case 'submit':
            if len(args) not in (3, 4):
                raise ValidationError('submit студент работа балл [комментарий]')
            comment = args[3] if len(args) == 4 else ''
            return course.submit(args[0], args[1], float(args[2]), comment)
        case 'submission':
            if len(args) not in (4, 5) or args[0] not in ('accept', 'reject'):
                raise ValidationError('submission accept/reject студент работа номер [причина]')
            status = 'accepted' if args[0] == 'accept' else 'rejected'
            comment = args[4] if len(args) == 5 else ''
            course.set_status(args[1], args[2], int(args[3]), status, comment)
            return 'Статус попытки изменен.'
        case 'history':
            if len(args) != 1:
                raise ValidationError('history студент')
            course.get_student(args[0])
            return list(course.submissions_for(args[0]))
        case 'report':
            return report_command(course, args)
        case 'top':
            if len(args) > 1:
                raise ValidationError('top [число]')
            return course.rating(int(args[0]) if args else 5)
        case 'import':
            if len(args) != 2:
                raise ValidationError('import students/submissions путь.csv')
            return import_csv(course, args[0], args[1])
        case 'export':
            if len(args) != 2:
                raise ValidationError('export json/csv путь')
            if args[0] == 'json':
                save_course(course, args[1])
            elif args[0] == 'csv':
                export_csv(course, args[1])
            else:
                raise ValidationError('Формат: json или csv')
            return 'Экспорт выполнен.'
        case 'save' | 'exit':
            if args:
                raise ValidationError('Эта команда не принимает аргументы')
            save_course(course, state_path)
            return 'Данные сохранены.'
        case 'snapshot':
            if args == ['create']:
                course.create_snapshot()
            elif args == ['restore']:
                course.restore_snapshot()
            else:
                raise ValidationError('snapshot create/restore')
            return 'Команда снимка выполнена.'
        case 'undo':
            if args:
                raise ValidationError('undo не принимает аргументы')
            course.undo()
            return 'Последнее изменение отменено.'
        case 'memory':
            if args == ['profile']:
                return profile_reports(course)
            if not args:
                return memory_report(course)
            raise ValidationError('memory [profile]')
        case _:
            raise ValidationError('Неизвестная команда. Введите help.')


def handle_line(course, line, state_path):
    """Неудачная команда восстанавливает состояние; успешная поддерживает undo."""
    parts = shlex.split(line)
    if not parts:
        return '', False
    # undo не должен сам создавать новую запись отмены.
    if parts[0] == 'undo' or parts == ['snapshot', 'create']:
        result = execute(course, parts, state_path)
    else:
        with course.transaction():
            result = execute(course, parts, state_path)
    return result, parts[0] == 'exit'


def main():
    state_path = Path('data/course.json')
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(filename='logs/course_tracker.log', encoding='utf-8',
                        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    tracemalloc.start()
    try:
        course = load_course(state_path)
    except CourseTrackerError as error:
        print(error)
        print('Запуск остановлен, чтобы не затереть поврежденный файл.')
        return
    print('CourseTracker 1.0\nВведите help для просмотра команд.')
    while True:
        try:
            line = input('course-tracker> ')
        except EOFError:
            line = 'exit'
        except KeyboardInterrupt:
            print('\nДля сохранения и выхода введите exit.')
            continue
        try:
            result, finished = handle_line(course, line, state_path)
            print(result)
            if finished:
                break
        except (CourseTrackerError, ValueError, IndexError, TypeError) as error:
            print('Ошибка:', error)
            logging.warning('Команда отклонена: %s', error)
            # При EOF не повторяем неудачный exit бесконечно.
            if line == 'exit':
                break
    tracemalloc.stop()
