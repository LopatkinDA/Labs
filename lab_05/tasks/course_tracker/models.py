"""Простые модели предметной области."""
from dataclasses import dataclass, field
from datetime import date, datetime
from math import isfinite
from .exceptions import ValidationError


def check_id(value):
    """Идентификатор — непустая строка без пробельных символов."""
    if not isinstance(value, str) or not value:
        raise ValidationError('Идентификатор не может быть пустым')
    for symbol in value:
        if symbol.isspace():
            raise ValidationError('В идентификаторе нельзя использовать пробелы')


@dataclass
class Student:
    """Студент остается в истории после деактивации."""
    student_id: str
    full_name: str
    group: str
    registered_at: str = field(default_factory=lambda: date.today().isoformat())
    active: bool = True

    def __post_init__(self):
        check_id(self.student_id)
        if not isinstance(self.full_name, str) or not self.full_name.strip():
            raise ValidationError('Имя не может быть пустым')
        self.full_name = ' '.join(self.full_name.split())
        if not isinstance(self.group, str) or not self.group.strip():
            raise ValidationError('Группа не может быть пустой')
        if not isinstance(self.active, bool):
            raise ValidationError('active должен быть логическим значением')
        try:
            date.fromisoformat(self.registered_at)
        except (ValueError, TypeError):
            raise ValidationError('Неверная дата регистрации')


@dataclass
class Laboratory:
    """Описание лабораторной и допустимый максимум баллов."""
    laboratory_id: str
    title: str
    max_score: float
    deadline: str
    tags: set = field(default_factory=set)
    description: str = ''

    def __post_init__(self):
        check_id(self.laboratory_id)
        if not self.title.strip():
            raise ValidationError('Название не может быть пустым')
        if not isfinite(self.max_score) or self.max_score <= 0:
            raise ValidationError('Максимальный результат должен быть положительным')
        try:
            date.fromisoformat(self.deadline)
        except (ValueError, TypeError):
            raise ValidationError('Дата должна иметь вид ГГГГ-ММ-ДД')
        cleaned = set()
        for tag in self.tags:
            tag = tag.strip().lower()
            if tag:
                cleaned.add(tag)
        self.tags = cleaned


@dataclass
class Submission:
    """Одна попытка сдачи. Максимум передается из лабораторной."""
    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ''
    status: str = 'submitted'
    submitted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    max_score: float = 100

    def __post_init__(self):
        check_id(self.student_id)
        check_id(self.laboratory_id)
        if not isinstance(self.attempt, int) or self.attempt <= 0:
            raise ValidationError('Номер попытки должен быть положительным целым')
        if not isfinite(self.max_score) or self.max_score <= 0:
            raise ValidationError('Неверный максимум баллов')
        if not isfinite(self.score) or not 0 <= self.score <= self.max_score:
            raise ValidationError('Балл выходит за допустимый диапазон')
        if self.status not in ('submitted', 'accepted', 'rejected'):
            raise ValidationError('Неверный статус попытки')
        try:
            datetime.fromisoformat(self.submitted_at)
        except (ValueError, TypeError):
            raise ValidationError('Неверные дата и время попытки')
