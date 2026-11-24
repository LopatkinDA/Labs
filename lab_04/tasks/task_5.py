"""Журнал курса: наследование, композиция и протоколы."""
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator
from datetime import datetime
from task_4 import Course, Student, Submission


class CourseEvent(ABC):
    """Общий интерфейс события курса."""

    def __init__(self, student_id: str) -> None:
        """Запоминаем студента и время создания."""
        self._student_id = student_id
        self.created_at = datetime.now()

    @property
    @abstractmethod
    def student_id(self) -> str:
        """Идентификатор студента события."""
        raise NotImplementedError

    @abstractmethod
    def describe(self) -> str:
        """Описание события для временной шкалы."""
        raise NotImplementedError


class SubmissionEvent(CourseEvent):
    """Событие содержит запись попытки сдачи."""

    def __init__(self, submission: Submission) -> None:
        """Сохраняем попытку как составную часть события."""
        super().__init__(submission.student_id)
        self.submission = submission

    @property
    def student_id(self) -> str:
        """Возвращаем идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Описываем работу, попытку и балл."""
        s = self.submission
        return f'{s.student_id}: {s.laboratory_id}, попытка {s.attempt}, балл {s.score}'


class AttendanceEvent(CourseEvent):
    """Событие посещения занятия."""

    def __init__(self, student_id: str, lesson: str) -> None:
        """Запоминаем название посещенного занятия."""
        super().__init__(student_id)
        self.lesson = lesson

    @property
    def student_id(self) -> str:
        """Возвращаем идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Описываем посещение."""
        return f'{self.student_id}: посетил занятие {self.lesson}'


class CommentEvent(CourseEvent):
    """Текстовая обратная связь."""

    def __init__(self, student_id: str, text: str) -> None:
        """Запоминаем текст отзыва."""
        super().__init__(student_id)
        self.text = text

    @property
    def student_id(self) -> str:
        """Возвращаем идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Описываем отзыв."""
        return f'{self.student_id}: отзыв — {self.text}'


class DeadlineEvent(CourseEvent):
    """Новый вид события, не требующий изменения render_timeline."""

    def __init__(self, student_id: str, deadline: str) -> None:
        """Запоминаем срок сдачи."""
        super().__init__(student_id)
        self.deadline = deadline

    @property
    def student_id(self) -> str:
        """Возвращаем идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Описываем срок."""
        return f'{self.student_id}: срок сдачи {self.deadline}'


class CourseJournal:
    """Упорядоченная коллекция событий."""

    def __init__(self) -> None:
        """Создаем внутренний список."""
        self._events = []

    def add(self, event: CourseEvent) -> None:
        """Добавляем событие в конец."""
        self._events.append(event)

    def __len__(self) -> int:
        """Число событий."""
        return len(self._events)

    def __iter__(self) -> Iterator[CourseEvent]:
        """Независимый последовательный обход."""
        return iter(self._events)

    def __getitem__(self, index: int | slice) -> CourseEvent | list[CourseEvent]:
        """Поддерживаем индекс и срез; срез создает новый список."""
        return self._events[index]

    def __str__(self) -> str:
        """Краткая информация для пользователя."""
        return f'Журнал: {len(self)} событий'

    def __repr__(self) -> str:
        """Краткая информация для отладки."""
        return f'CourseJournal(events={len(self)})'

    def events_for_student(self, student_id: str) -> Iterator[CourseEvent]:
        """Ленивая выборка по студенту."""
        for event in self:
            if event.student_id == student_id:
                yield event

    def events_by_type(self, event_type: type) -> Iterator[CourseEvent]:
        """Ленивая выборка по типу."""
        for event in self:
            if isinstance(event, event_type):
                yield event

    def summary(self) -> dict:
        """Возвращаем новый словарь счетчиков."""
        counts = {}
        for event in self:
            name = type(event).__name__
            counts[name] = counts.get(name, 0) + 1
        return counts


def render_timeline(events: Iterable[CourseEvent]) -> str:
    """Работаем с общим интерфейсом describe без проверки типов."""
    lines = []
    for event in events:
        lines.append(event.created_at.isoformat(timespec='seconds') + ' ' + event.describe())
    return '\n'.join(lines)


class ScoreView:
    """Повторно обходимый ленивый вид только баллов сдач."""

    def __init__(self, journal: CourseJournal) -> None:
        """Сохраняем ссылку на журнал, не копируем события."""
        self.journal = journal

    def __iter__(self) -> Iterator[float]:
        """Новый генератор при каждом обходе."""
        for event in self.journal:
            if isinstance(event, SubmissionEvent):
                yield event.submission.score


class FilteredJournalView:
    """Ленивая выборка по переданному условию."""

    def __init__(self, journal: CourseJournal,
                 predicate: Callable[[CourseEvent], bool]) -> None:
        """Сохраняем журнал и функцию условия."""
        self.journal = journal
        self.predicate = predicate

    def __iter__(self) -> Iterator[CourseEvent]:
        """Повторный обход снова проверяет условие."""
        for event in self.journal:
            if self.predicate(event):
                yield event


def is_anna(event: CourseEvent) -> bool:
    """Именованный предикат для студента s1."""
    return event.student_id == 's1'


def main() -> None:
    """Создаем трех студентов и одиннадцать событий."""
    course = Course()
    for sid, name in [('s1', 'Анна'), ('s2', 'Борис'), ('s3', 'Дарья')]:
        course.add_student(Student(sid, name))
    journal = CourseJournal()
    for sid in ['s1', 's2', 's3']:
        journal.add(AttendanceEvent(sid, 'Python'))
        journal.add(CommentEvent(sid, 'Продолжайте работу'))
    for sid, score in [('s1', 70), ('s1', 90), ('s2', 80), ('s3', 100)]:
        journal.add(SubmissionEvent(course.submit(sid, 'lab_01', score)))
    journal.add(DeadlineEvent('s1', '2026-12-01'))
    assert len(course) == 3 and len(journal) == 11
    print(str(journal), repr(journal))
    print(render_timeline(journal))
    print('Студент s1:', render_timeline(journal.events_for_student('s1')))
    assert len(list(journal.events_for_student('s1'))) == 5
    assert len(list(journal.events_by_type(SubmissionEvent))) == 4
    part = journal[:2]
    part.clear()
    assert len(journal) == 11
    assert journal[0] is list(journal)[0]
    counts = journal.summary()
    counts.clear()
    assert journal.summary()['SubmissionEvent'] == 4
    scores = ScoreView(journal)
    assert list(scores) == list(scores) == [70, 90, 80, 100]
    print('Баллы:', list(scores), 'среднее:', sum(scores) / len(list(scores)))
    named = FilteredJournalView(journal, is_anna)
    unnamed = FilteredJournalView(journal, lambda event: event.student_id == 's1')
    assert list(named) == list(named) == list(unnamed)
    print('Журнал и представления: проверки пройдены')


if __name__ == '__main__':
    main()
