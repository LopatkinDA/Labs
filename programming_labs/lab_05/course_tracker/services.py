"""Регистрация, попытки, поиск, отчеты и отмена."""
from contextlib import contextmanager
from copy import deepcopy
from .models import Student, Laboratory, Submission
from .exceptions import ValidationError, DuplicateError, NotFoundError
from .utils import log_action


class Course:
    """Курс хранит словари студентов и работ, а также историю попыток."""

    def __init__(self):
        self.students = {}
        self.laboratories = {}
        self.submissions = []
        self._undo = []
        self._snapshot = None

    def __len__(self):
        return len(self.students)

    def __iter__(self):
        return iter(self.students.values())

    def __contains__(self, student_id):
        return student_id in self.students

    def __getitem__(self, student_id):
        return self.get_student(student_id)

    def get_student(self, student_id):
        if student_id not in self.students:
            raise NotFoundError('Студент не найден: ' + student_id)
        return self.students[student_id]

    def get_lab(self, laboratory_id):
        if laboratory_id not in self.laboratories:
            raise NotFoundError('Работа не найдена: ' + laboratory_id)
        return self.laboratories[laboratory_id]

    @log_action
    def add_student(self, student):
        if student.student_id in self.students:
            raise DuplicateError('Студент уже зарегистрирован')
        self.students[student.student_id] = student

    @log_action
    def add_lab(self, laboratory):
        if laboratory.laboratory_id in self.laboratories:
            raise DuplicateError('Работа уже существует')
        self.laboratories[laboratory.laboratory_id] = laboratory

    @log_action
    def set_active(self, student_id, active):
        self.get_student(student_id).active = active

    def submissions_for(self, student_id=None, laboratory_id=None):
        """Новый генератор при каждом вызове."""
        for submission in self.submissions:
            if student_id is not None and submission.student_id != student_id:
                continue
            if laboratory_id is not None and submission.laboratory_id != laboratory_id:
                continue
            yield submission

    @log_action
    def submit(self, student_id, laboratory_id, score, comment=''):
        student = self.get_student(student_id)
        laboratory = self.get_lab(laboratory_id)
        if not student.active:
            raise ValidationError('Студент неактивен')
        attempt = 1
        for old in self.submissions_for(student_id, laboratory_id):
            if old.attempt >= attempt:
                attempt = old.attempt + 1
        submission = Submission(student_id, laboratory_id, attempt, score,
                                comment, max_score=laboratory.max_score)
        self.submissions.append(submission)
        return submission

    @log_action
    def set_status(self, student_id, laboratory_id, attempt, status, comment=''):
        if status not in ('accepted', 'rejected'):
            raise ValidationError('Неверный статус')
        for submission in self.submissions_for(student_id, laboratory_id):
            if submission.attempt == attempt:
                submission.status = status
                if comment:
                    submission.comment = comment
                return
        raise NotFoundError('Попытка не найдена')

    def list_students(self, sort_by='name'):
        if sort_by == 'name':
            return sorted(self.students.values(), key=lambda s: s.full_name.lower())
        if sort_by == 'group':
            return sorted(self.students.values(), key=lambda s: (s.group, s.full_name))
        if sort_by == 'id':
            return sorted(self.students.values(), key=lambda s: s.student_id)
        raise ValidationError('Сортировка: name, group или id')

    def search_students(self, text):
        result = []
        for student in self:
            if text.lower() in student.full_name.lower():
                result.append(student)
        return result

    def search_labs(self, text):
        result = []
        for lab in self.laboratories.values():
            content = lab.title + ' ' + lab.description + ' ' + ' '.join(lab.tags)
            if text.lower() in content.lower():
                result.append(lab)
        return result

    def student_summary(self, student_id):
        """Среднее и максимум считаем по всем попыткам; прогресс — по принятым."""
        student = self.get_student(student_id)
        scores = []
        accepted = set()
        best_by_lab = {}
        for submission in self.submissions_for(student_id):
            scores.append(submission.score)
            lab_id = submission.laboratory_id
            if lab_id not in best_by_lab or submission.score > best_by_lab[lab_id]:
                best_by_lab[lab_id] = submission.score
            if submission.status == 'accepted':
                accepted.add(lab_id)
        missing = sorted(set(self.laboratories) - accepted)
        # Для рейтинга приводим максимум каждой работы к 100 процентам.
        percent_total = 0
        for lab_id, score in best_by_lab.items():
            percent_total += score / self.laboratories[lab_id].max_score * 100
        rating_score = None
        if self.laboratories:
            rating_score = percent_total / len(self.laboratories)
        average = None
        best = None
        if scores:
            average = sum(scores) / len(scores)
            best = max(scores)
        return {'student_id': student_id, 'name': student.full_name,
                'attempts': len(scores), 'best': best, 'mean': average,
                'completed': len(accepted), 'total_labs': len(self.laboratories),
                'missing': missing, 'best_by_lab': best_by_lab,
                'rating_score': rating_score}

    def report_rows(self):
        """Лениво выдаем по одной сводке студента."""
        for student_id in self.students:
            yield self.student_summary(student_id)

    def rating(self, limit=None):
        rows = list(self.report_rows())
        # Собственная сортировка выбором по убыванию процента.
        for i in range(len(rows)):
            best = i
            for j in range(i + 1, len(rows)):
                left = rows[j]['rating_score']
                right = rows[best]['rating_score']
                if left is None:
                    left = -1
                if right is None:
                    right = -1
                if left > right:
                    best = j
            rows[i], rows[best] = rows[best], rows[i]
        if limit is None:
            return rows
        if limit < 0:
            raise ValidationError('Лимит не может быть отрицательным')
        if limit == 0 or limit >= len(rows):
            return rows[:limit]
        cutoff = rows[limit - 1]['rating_score']
        result = rows[:limit]
        for row in rows[limit:]:
            if row['rating_score'] == cutoff:
                result.append(row)
        return result

    def group_summary(self):
        categories = {'0-59': 0, '60-74': 0, '75-89': 0,
                      '90-100': 0, 'нет работ': 0}
        for row in self.report_rows():
            score = row['rating_score']
            if score is None:
                category = 'нет работ'
            elif score >= 90:
                category = '90-100'
            elif score >= 75:
                category = '75-89'
            elif score >= 60:
                category = '60-74'
            else:
                category = '0-59'
            categories[category] += 1
        scores = []
        for submission in self.submissions:
            scores.append(submission.score)
        average = None
        best = None
        if scores:
            average = sum(scores) / len(scores)
            best = max(scores)
        ranking = self.rating()
        leaders = []
        if ranking and ranking[0]['rating_score'] is not None:
            for row in ranking:
                if row['rating_score'] == ranking[0]['rating_score']:
                    leaders.append(row['student_id'])
        return {'students': len(self), 'attempts': len(scores),
                'mean': average, 'best': best, 'categories': categories,
                'leaders': leaders, 'rating': ranking}

    def lab_summary(self, laboratory_id):
        lab = self.get_lab(laboratory_id)
        scores = []
        accepted = set()
        for submission in self.submissions_for(laboratory_id=laboratory_id):
            scores.append(submission.score)
            if submission.status == 'accepted':
                accepted.add(submission.student_id)
        return {'laboratory_id': lab.laboratory_id, 'attempts': len(scores),
                'best': max(scores) if scores else None,
                'mean': sum(scores) / len(scores) if scores else None,
                'accepted_students': len(accepted)}

    def state(self):
        """Копируем только данные, без рекурсивного копирования истории undo."""
        return deepcopy({'students': self.students,
                         'laboratories': self.laboratories,
                         'submissions': self.submissions})

    def restore_state(self, state):
        data = deepcopy(state)
        self.students = data['students']
        self.laboratories = data['laboratories']
        self.submissions = data['submissions']

    @contextmanager
    def transaction(self):
        """Откатываем неудачную команду, успешную запоминаем для undo."""
        before = self.state()
        try:
            yield
        except Exception:
            self.restore_state(before)
            raise
        else:
            if self.state() != before:
                self._undo.append(before)

    def undo(self):
        if not self._undo:
            raise ValidationError('Нет изменений для отмены')
        self.restore_state(self._undo.pop())

    def create_snapshot(self):
        self._snapshot = self.state()

    def restore_snapshot(self):
        if self._snapshot is None:
            raise ValidationError('Снимок еще не создан')
        self.restore_state(self._snapshot)
