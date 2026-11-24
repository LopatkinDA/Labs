"""Анализ памяти текущего курса и ленивого отчета."""
import gc
import sys
import tracemalloc


def memory_report(course):
    """Показываем число объектов и размеры внешних коллекций."""
    current, peak = tracemalloc.get_traced_memory()
    return {
        'students': len(course.students),
        'laboratories': len(course.laboratories),
        'submissions': len(course.submissions),
        'students_bytes': sys.getsizeof(course.students),
        'laboratories_bytes': sys.getsizeof(course.laboratories),
        'submissions_bytes': sys.getsizeof(course.submissions),
        'current_bytes': current,
        'peak_bytes': peak,
    }


def profile_reports(course):
    """Сравниваем одинаковые сводки списком и генератором."""
    results = []
    was_tracing = tracemalloc.is_tracing()
    tracemalloc.stop()
    for mode in ('list', 'generator'):
        gc.collect()
        tracemalloc.start()
        if mode == 'list':
            rows = list(course.report_rows())
        else:
            rows = course.report_rows()
        count = 0
        for row in rows:
            count += 1
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        results.append({'mode': mode, 'rows': count, 'peak_bytes': peak})
        del rows
    if was_tracing:
        tracemalloc.start()
    return results
