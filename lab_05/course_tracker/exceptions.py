"""Понятные ошибки приложения."""


class CourseTrackerError(Exception):
    """Общая ошибка приложения."""


class ValidationError(CourseTrackerError):
    """Неверные данные."""


class DuplicateError(CourseTrackerError):
    """Идентификатор уже занят."""


class NotFoundError(CourseTrackerError):
    """Запись не найдена."""


class StorageError(CourseTrackerError):
    """Ошибка чтения или записи файла."""
