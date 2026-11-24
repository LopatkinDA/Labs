"""Студенты, попытки сдачи и курс."""
from dataclasses import dataclass
from collections.abc import Iterator
from math import isfinite


@dataclass(frozen=True)
class Submission:
    """Неизменяемая запись одной попытки."""
    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ''

    def __post_init__(self) -> None:
        """Проверяем идентификаторы, номер и диапазон балла."""
        if not self.student_id.strip() or not self.laboratory_id.strip():
            raise ValueError('Идентификаторы не могут быть пустыми')
        if self.attempt <= 0:
            raise ValueError('Номер попытки должен быть положительным')
        if not isfinite(self.score) or not 0 <= self.score <= 100:
            raise ValueError('Балл должен быть от 0 до 100')


class Student:
    """Хранит данные студента и его попытки."""

    def __init__(self, student_id: str, full_name: str) -> None:
        """Создаем студента с пустой историей."""
        if not self.valid_id(student_id) or not full_name.strip():
            raise ValueError('Неверный идентификатор или пустое имя')
        self.student_id = student_id
        self.full_name = full_name
        self._submissions = []

    @staticmethod
    def valid_id(student_id: str) -> bool:
        """Идентификатор непустой и не содержит пробельных символов."""
        return bool(student_id) and len(student_id.split()) == 1 and not any(
            symbol.isspace() for symbol in student_id)

    @classmethod
    def from_full_name(cls, student_id: str, full_name: str) -> 'Student':
        """Убираем лишние пробелы в имени."""
        return cls(student_id, ' '.join(full_name.split()))

    def add_submission(self, submission: Submission) -> None:
        """Добавляем только попытку данного студента без дубля номера."""
        if submission.student_id != self.student_id:
            raise ValueError('Попытка принадлежит другому студенту')
        for old in self._submissions:
            if (old.laboratory_id == submission.laboratory_id
                    and old.attempt == submission.attempt):
                raise ValueError('Попытка с таким номером уже есть')
        self._submissions.append(submission)

    @property
    def submissions(self) -> tuple[Submission, ...]:
        """Выдаем кортеж вместо внутреннего изменяемого списка."""
        return tuple(self._submissions)

    @property
    def average_score(self) -> float | None:
        """Среднее всех попыток или None, если попыток нет."""
        if not self._submissions:
            return None
        total = 0
        for submission in self._submissions:
            total += submission.score
        return total / len(self._submissions)

    def best_score(self, laboratory_id: str) -> float | None:
        """Лучший балл указанной работы или None."""
        best = None
        for submission in self._submissions:
            if submission.laboratory_id == laboratory_id:
                if best is None or submission.score > best:
                    best = submission.score
        return best

    def __len__(self) -> int:
        """Число попыток."""
        return len(self._submissions)

    def __iter__(self) -> Iterator[Submission]:
        """Независимый обход истории."""
        return iter(self._submissions)

    def __str__(self) -> str:
        """Представление для пользователя."""
        return f'{self.full_name}: {len(self)} попыток'

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f'Student({self.student_id!r}, {self.full_name!r})'


class Course:
    """Хранит студентов и управляет сдачей работ."""

    def __init__(self) -> None:
        """Создаем пустой курс."""
        self._students = {}

    def add_student(self, student: Student) -> None:
        """Регистрируем уникальный идентификатор."""
        if student.student_id in self._students:
            raise ValueError('Студент уже зарегистрирован')
        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        """Находим студента или вызываем KeyError."""
        return self._students[student_id]

    def submit(self, student_id: str, laboratory_id: str,
               score: float, comment: str = '') -> Submission:
        """Автоматически назначаем следующий номер попытки."""
        student = self.get_student(student_id)
        attempt = 1
        for old in student:
            if old.laboratory_id == laboratory_id:
                attempt = max(attempt, old.attempt + 1)
        submission = Submission(student_id, laboratory_id, attempt, score, comment)
        student.add_submission(submission)
        return submission

    def top_students(self, limit: int = 3) -> list[Student]:
        """Возвращаем студентов с оценками по убыванию среднего."""
        if limit < 0:
            raise ValueError('Лимит не может быть отрицательным')
        students = []
        for student in self:
            if student.average_score is not None:
                students.append(student)
        return sorted(students, key=lambda s: s.average_score, reverse=True)[:limit]

    def __contains__(self, student_id: str) -> bool:
        """Проверяем наличие идентификатора."""
        return student_id in self._students

    def __len__(self) -> int:
        """Число зарегистрированных студентов."""
        return len(self._students)

    def __iter__(self) -> Iterator[Student]:
        """Обходим студентов в порядке регистрации."""
        return iter(self._students.values())


def main() -> None:
    """Проверяем свойства, конструкторы и стандартные операции."""
    course = Course()
    anna = Student.from_full_name('s1', '  Анна   Смирнова ')
    course.add_student(anna)
    course.add_student(Student('s2', 'Борис Иванов'))
    first = course.submit('s1', 'lab_01', 70)
    second = course.submit('s1', 'lab_01', 90)
    course.submit('s2', 'lab_01', 95)
    assert anna.full_name == 'Анна Смирнова'
    assert first == Submission('s1', 'lab_01', 1, 70)
    assert len(anna) == 2 and anna.average_score == 80
    assert anna.best_score('lab_01') == 90
    assert anna.best_score('unknown') is None
    assert isinstance(anna.submissions, tuple)
    assert len(course) == 2 and 's1' in course
    a = iter(anna)
    b = iter(anna)
    assert next(a) is next(b) is first
    before = anna.submissions
    ordered = sorted(anna, key=lambda s: (s.attempt, s.score))
    by_score = sorted(anna, key=lambda s: s.score, reverse=True)
    assert anna.submissions == before
    assert by_score[0] is second
    print(str(anna), repr(anna), ordered, by_score)
    print('Курс:', len(course), 's1' in course, list(course))
    print('Рейтинг:', course.top_students())
    for bad in [('s1', '', 1, 50), ('s1', 'lab', 0, 50), ('s1', 'lab', 1, 101)]:
        try:
            Submission(*bad)
        except ValueError as error:
            print('Отклонено:', error)
        else:
            raise AssertionError('Неверная попытка принята')
    print('Модель: проверки пройдены')


if __name__ == '__main__':
    main()
