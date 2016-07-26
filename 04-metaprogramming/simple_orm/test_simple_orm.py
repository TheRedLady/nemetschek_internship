import unittest
import collections
from mock import Mock

import simple_orm as model


class Question(model.Model):
    count = model.IntField()


class Student(model.Model):
    name = model.CharField()
    marks = model.CharField()


class TestModel(unittest.TestCase):

    def test_setup(self):
        cursor = Mock()
        Question.setup_schema(cursor)
        cursor.execute.assert_called_with(
            'CREATE TABLE question (id INTEGER PRIMARY KEY AUTOINCREMENT, count INTEGER)')

    def test_save(self):
        cursor = Mock(lastrowid=1)
        q = Question(cursor, count=1)
        q.save()
        cursor.execute.assert_called_with(
            'INSERT INTO question (count) VALUES (:count)', {'count': 1})

    def test_update(self):
        cursor = Mock(lastrowid=1)
        q = Question(cursor, count=1, id=1)
        q.save()
        cursor.execute.assert_called_with(
            'UPDATE question SET count = :count WHERE id = :id', {'count': 1, 'id': 1})

    def test_validation(self):
        q = Question(None)
        q.count = 1
        with self.assertRaises(model.ValidationError):
            q.count = 'z'

    def test_char_filed(self):
        class Answer(model.Model):

            text = model.CharField(max_length=10)

        a = Answer(None)
        a.text = 'a'
        with self.assertRaises(model.ValidationError):
            a.text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'

    def test_bool_field(self):
        class Statement(model.Model):

            is_true = model.BooleanField()

        s = Statement(None, is_true=False)
        s.is_true = True
        with self.assertRaises(model.ValidationError):
            s.is_true = 5
        self.assertTrue(s.is_true)

    def test_filter(self):
        cursor = Mock()
        Student.filter(cursor, Student.name == 'Ivan')
        cursor.execute.assert_called_with(
            'SELECT * FROM student WHERE name = :name',
            {'name': 'Ivan'})
        Student.filter(cursor, Student.name != 'Ivan')
        cursor.execute.assert_called_with(
            'SELECT * FROM student WHERE NOT name = :name',
            {'name': 'Ivan'})
        Student.filter(
            cursor, model.Field.or_(
                Student.name == 'Ivan', Student.name == 'Peter'),
        )
        cursor.execute.assert_called_with(
            'SELECT * FROM student WHERE name = ? OR name = ?',
            ('Ivan',
             'Peter'))
        Student.filter(
            cursor, Student.name.startswith('I'),
        )
        cursor.execute.assert_called_with(
            'SELECT * FROM student WHERE name LIKE ":name%"',
            {'name': 'I'})

    def test_db(self):
        Student.cursor = Mock()
        Student.select().where(Student.name == 'Ivan').get()
        Student.cursor.execute.assert_called_with(
            'SELECT * FROM user WHERE name = :name', {'name': 'Ivan'})

        with self.assertRaises(model.MultipleResultsError):
            Student.select().where(Student.name == 'Ivan').one()

        Student.select().where(Student.name == 'Ivan').first()
        Student.cursor.execute.assert_called_with(
            'SELECT * FROM user WHERE name = :name', {'name': 'Ivan'})


if __name__ == '__main__':
    unittest.main()
