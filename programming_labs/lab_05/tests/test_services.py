import pytest
from course_tracker.models import Student, Laboratory
from course_tracker.services import Course
from course_tracker.exceptions import DuplicateError, ValidationError, NotFoundError


def example_course():
    course = Course()
    course.add_student(Student('s1', 'Анна', 'P3120'))
    course.add_lab(Laboratory('lab1', 'Типы', 100, '2026-12-01'))
    return course


def test_duplicate_student_is_rejected():
    course = example_course()
    with pytest.raises(DuplicateError):
        course.add_student(Student('s1', 'Другая Анна', 'P3120'))


def test_attempt_numbers_and_best_score():
    course = example_course()
    first = course.submit('s1', 'lab1', 70)
    second = course.submit('s1', 'lab1', 90)
    assert first.attempt == 1
    assert second.attempt == 2
    assert course.student_summary('s1')['best'] == 90


def test_student_average():
    course = example_course()
    course.submit('s1', 'lab1', 70)
    course.submit('s1', 'lab1', 90)
    assert course.student_summary('s1')['mean'] == pytest.approx(80)


def test_missing_requires_accepted_status():
    course = example_course()
    course.submit('s1', 'lab1', 90)
    assert course.student_summary('s1')['missing'] == ['lab1']
    course.set_status('s1', 'lab1', 1, 'accepted')
    assert course.student_summary('s1')['missing'] == []


def test_unknown_student_is_rejected():
    course = example_course()
    with pytest.raises(NotFoundError):
        course.submit('unknown', 'lab1', 50)


def test_score_uses_laboratory_maximum():
    course = example_course()
    course.add_lab(Laboratory('lab2', 'Тест', 10, '2026-12-01'))
    with pytest.raises(ValidationError):
        course.submit('s1', 'lab2', 11)


def test_empty_student_and_course():
    assert Course().group_summary()['mean'] is None
    course = example_course()
    assert course.student_summary('s1')['mean'] is None


def test_equal_leaders_are_included_in_top():
    course = example_course()
    course.add_student(Student('s2', 'Борис', 'P3120'))
    course.submit('s1', 'lab1', 80)
    course.submit('s2', 'lab1', 80)
    assert len(course.rating(1)) == 2
    assert course.group_summary()['leaders'] == ['s1', 's2']


def test_snapshot_is_independent():
    course = example_course()
    course.create_snapshot()
    course.set_active('s1', False)
    course.restore_snapshot()
    assert course.get_student('s1').active is True
    assert course.submissions == []


def test_failed_transaction_restores_state():
    course = example_course()
    with pytest.raises(ValidationError):
        with course.transaction():
            course.add_student(Student('s2', 'Борис', 'P3120'))
            course.submit('s1', 'lab1', 101)
    assert 's2' not in course
    assert course.submissions == []


def test_undo_restores_last_successful_change():
    course = example_course()
    with course.transaction():
        course.submit('s1', 'lab1', 50)
    course.undo()
    assert course.submissions == []


def test_repeated_and_independent_iteration():
    course = example_course()
    course.submit('s1', 'lab1', 50)
    first = course.submissions_for('s1')
    second = course.submissions_for('s1')
    assert next(first) is next(second)
    assert len(list(course.submissions_for('s1'))) == 1
    assert len(list(course)) == len(course) == 1


def test_inactive_student_keeps_history():
    course = example_course()
    course.submit('s1', 'lab1', 50)
    course.set_active('s1', False)
    assert len(list(course.submissions_for('s1'))) == 1
    with pytest.raises(ValidationError):
        course.submit('s1', 'lab1', 60)
