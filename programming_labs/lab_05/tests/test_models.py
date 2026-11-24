import pytest
from course_tracker.models import Student, Laboratory, Submission
from course_tracker.exceptions import ValidationError


def test_student_is_created():
    student = Student('s001', 'Анна Смирнова', 'P3120')
    assert student.student_id == 's001'
    assert student.full_name == 'Анна Смирнова'
    assert student.active is True


def test_student_rejects_empty_id():
    with pytest.raises(ValidationError):
        Student('', 'Анна', 'P3120')


def test_student_rejects_empty_name():
    with pytest.raises(ValidationError):
        Student('s001', ' ', 'P3120')


def test_student_rejects_space_in_id():
    with pytest.raises(ValidationError):
        Student('s 001', 'Анна', 'P3120')


def test_laboratory_is_created():
    lab = Laboratory('lab_01', 'Типы', 100, '2026-12-01', {' Python ', 'python', ''})
    assert lab.max_score == 100
    assert lab.tags == {'python'}


def test_laboratory_rejects_zero_maximum():
    with pytest.raises(ValidationError):
        Laboratory('lab_01', 'Типы', 0, '2026-12-01')


def test_submission_rejects_large_score():
    with pytest.raises(ValidationError):
        Submission('s001', 'lab_01', 1, 101)


def test_submission_rejects_negative_score():
    with pytest.raises(ValidationError):
        Submission('s001', 'lab_01', 1, -1)


def test_submission_rejects_nan():
    with pytest.raises(ValidationError):
        Submission('s001', 'lab_01', 1, float('nan'))


def test_submission_rejects_zero_attempt():
    with pytest.raises(ValidationError):
        Submission('s001', 'lab_01', 0, 50)
