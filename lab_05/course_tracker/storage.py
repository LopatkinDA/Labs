"""JSON, CSV и атомарная запись файла."""
import csv
import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from .models import Student, Laboratory, Submission
from .services import Course
from .exceptions import CourseTrackerError, StorageError, ValidationError


def to_dict(course):
    students = []
    labs = []
    submissions = []
    for student in course:
        students.append(asdict(student))
    for lab in course.laboratories.values():
        row = asdict(lab)
        row['tags'] = sorted(lab.tags)
        labs.append(row)
    for submission in course.submissions:
        submissions.append(asdict(submission))
    return {'version': 1, 'students': students, 'laboratories': labs,
            'submissions': submissions, 'summary': course.group_summary()}


def from_dict(data):
    """Проверяем всю загрузку в новом объекте до замены рабочего курса."""
    course = Course()
    if data['version'] != 1:
        raise ValidationError('Неизвестная версия файла')
    for row in data['students']:
        course.add_student(Student(**row))
    for row in data['laboratories']:
        course.add_lab(Laboratory(**row))
    used = set()
    for row in data['submissions']:
        submission = Submission(**row)
        course.get_student(submission.student_id)
        lab = course.get_lab(submission.laboratory_id)
        if submission.max_score != lab.max_score:
            raise ValidationError('Максимум попытки не совпал с работой')
        key = (submission.student_id, submission.laboratory_id, submission.attempt)
        if key in used:
            raise ValidationError('Повтор номера попытки')
        used.add(key)
        course.submissions.append(submission)
    return course


def save_course(course, path):
    """Сначала пишем временный файл, затем заменяем основной через os.replace."""
    path = Path(path)
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(to_dict(course), ensure_ascii=False, indent=2, allow_nan=False)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=path.parent, delete=False) as file:
            temporary = Path(file.name)
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    except (OSError, ValueError, TypeError) as error:
        raise StorageError('Не удалось сохранить файл: ' + str(error)) from error
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def load_course(path):
    path = Path(path)
    if not path.exists():
        return Course()
    try:
        with path.open(encoding='utf-8') as file:
            data = json.load(file)
        return from_dict(data)
    except (OSError, ValueError, TypeError, KeyError, AttributeError,
            CourseTrackerError) as error:
        raise StorageError('Не удалось загрузить файл: ' + str(error)) from error


def import_csv(course, kind, path):
    """Каждую строку проверяем отдельно; ошибка строки не останавливает импорт."""
    accepted = 0
    rejected = []
    if kind not in ('students', 'submissions'):
        raise ValidationError('Импорт: students или submissions')
    try:
        with open(path, encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            for line, row in enumerate(reader, 2):
                try:
                    if kind == 'students':
                        student = Student(row['student_id'], row['full_name'], row['group'])
                        course.add_student(student)
                    else:
                        status = row.get('status', 'submitted') or 'submitted'
                        if status not in ('submitted', 'accepted', 'rejected'):
                            raise ValidationError('Неверный статус')
                        submission = course.submit(row['student_id'], row['laboratory_id'],
                                                   float(row['score']), row.get('comment', ''))
                        submission.status = status
                    accepted += 1
                except (CourseTrackerError, KeyError, ValueError, TypeError) as error:
                    rejected.append(f'Строка {line}: {error}')
    except (OSError, csv.Error, UnicodeError) as error:
        raise StorageError('Ошибка CSV: ' + str(error)) from error
    return {'accepted': accepted, 'rejected': len(rejected), 'errors': rejected}


def export_csv(course, path):
    """Экспортируем попытки; основные поля подходят для обратного импорта."""
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8-sig', newline='') as file:
            fields = ['student_id', 'laboratory_id', 'attempt', 'score',
                      'comment', 'status', 'submitted_at', 'max_score']
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for submission in course.submissions:
                writer.writerow(asdict(submission))
    except OSError as error:
        raise StorageError('Не удалось экспортировать CSV: ' + str(error)) from error
