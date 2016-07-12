import unittest
from mock import Mock

import simple_orm as model


class Question(model.Model):

    count = model.IntField()


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
            'INSERT INTO question (count) VALUES(:count)', {'count': 1})

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

            text = model.CharField(10)


        a = Answer(None)
        a.text = 'a'
        with self.assertRaises(model.ValidationError):
            a.text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'


if __name__ == '__main__':
    unittest.main()
