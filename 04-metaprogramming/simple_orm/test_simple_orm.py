import unittest
import collections
from mock import Mock
import sqlite3

import simple_orm as model


class Question(model.Model):
    count = model.IntField()


class Student(model.Model):
    name = model.CharField()
    marks = model.CharField()


class User(model.Model):
    name = model.CharField()
    age = model.IntField()
    is_active = model.BooleanField()

    class Meta:
        database = None


class TestModel(unittest.TestCase):

    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db_cursor = self.db.cursor()
        User.Meta.database = self.db
        db_cursor = self.db_cursor
        User.setup_schema(db_cursor)

        ivan = User(db_cursor, name='Ivan', age=20, is_active=False)
        ivan.save()
        ivan_ = User(db_cursor, name='Ivan', age=30, is_active=True)
        ivan_.save()
        maria = User(db_cursor, name='Maria', age=18, is_active=True)
        maria.save()
        petya = User(db_cursor, name='Petya', age=17, is_active=False)
        petya.save()
        lili = User(db_cursor, name='Lili', age=28, is_active=True)
        lili.save()
        todor = User(db_cursor, name='Todor', age=25, is_active=True)
        todor.save()
        biser = User(db_cursor, name='Biser', age=31, is_active=False)
        biser.save()

        User.cursor = self.db_cursor

    def tearDown(self):
        self.db_cursor.execute('DROP TABLE user')

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
        result = User.select().where(User.name == 'Ivan').get()
        User.cursor.execute.assert_called_with(
            'SELECT * FROM user WHERE name = :name', {'name': 'Ivan'})

        with self.assertRaises(model.MultipleResultsError):
            User.select().where(User.name == 'Ivan').one()

        result = User.select().where(User.name == 'Ivan').first()
        User.cursor.execute.assert_called_with(
            'SELECT * FROM user WHERE name = :name', {'name': 'Ivan'})
        self.assertIsInstance(result, model.Model)

        result = User.select().where(User.name == 'Pesho').first()
        self.assertIsNone(result)


    def test_select(self):
        User.cursor = self.db_cursor
        result = User.select().where(User.is_active == True).get()
        self.assertIsInstance(result, collections.Iterable)
        self.assertIsInstance(next(result), model.Model)

        result = User.select().where(User.name == 'Lili').one()
        self.assertEqual(result, lili)
        self.assertTrue(user.Meta.db_cursor.fetchone() is None)

        self.assertIsNone(User.select().where(User.name == 'Georgi').get())

        result = User.select().where(User.name.startswith('M')).get()
        self.assertEqual(next(result), maria)

        result = User.select().where(User.age.in_(17, 18)).get()
        result = [item for item in result]
        self.assertSetEqual(result, [maria, petya])

    def test_combine(self):
        result = User.select().where(or_(User.name == 'Ivan', User.age > 10)).get()
        result = [item for item in result]
        self.assertListEqual(result, self.users)

        result = User.select().where(and_(User.name == 'Ivan', User.age == 20)).get()
        result = [item for item in result]
        self.assertListEqual(result, [ivan])


    def test_limit(self):
        result = User.select().where(or_(User.is_active == True, User.age > 20)).limit(1).get()
        result = [item for item in result]
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()

