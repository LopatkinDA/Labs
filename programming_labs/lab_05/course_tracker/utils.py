"""Журналирование действий сервисного слоя."""
import logging
from functools import wraps


def log_action(function):
    """Декоратор сохраняет имя операции и ее результат в журнал."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('course_tracker')
        try:
            result = function(*args, **kwargs)
        except Exception:
            logger.warning('Ошибка операции %s', function.__name__)
            raise
        logger.info('Выполнена операция %s', function.__name__)
        return result
    return wrapper
