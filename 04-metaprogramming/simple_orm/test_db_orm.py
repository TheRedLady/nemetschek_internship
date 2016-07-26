import unittest
import collections
import sqlite3

import simple_orm as model


class SqliteDatabase(model.Cursor):

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)


db = sqlite3.connect(':memory:')


class User(model.Model):

    name = model.CharField()
    age = model.IntField()
    is_active = model.BooleanField()

    class Meta:
        database = db


ivan = User(name='Ivan', age=20, is_active=False)
ivan_ = User(name='Ivan', age=30, is_active=True)
maria = User(name='Maria', age=18, is_active=True)
petya = User(name='Petya', age=17, is_active=False)
lili = User(name='Lili', age=28, is_active=True)
todor = User(name='Todor', age=25, is_active=True)
biser = User(name='Biser', age=31, is_active=False)
stoyan = User(name='Stoyan', age=18, is_active=True)
nikol = User(name='Nikol', age=21, is_active=False)


class TestDB(unittest.TestCase):

    def setUp(self):
        self.users = [ivan, ivan_, maria, petya, lili, todor, biser, stoyan,
                      nikol]
        for user in self.users:
            user.save()

    def test_select(self):
        result_set = User.select().where(User.is_active).get()
        self.assertIsInstance(result_set, collections.Iterable)
        self.assertIsInstance(next(result_set), model.Model)
        self.assertIn(next(result_set), self.users)

        result_set = User.select().where(User.name == 'Lili').one()
        self.assertEqual(result_set, lili)

        with self.assertRaises(model.MultipleResultsError):
            User.select().where(User.name == 'Ivan').one()

        self.assertIsNone(User.select().where(User.name == 'Georgi').get())

        result_set = User.select().where(User.age.in_(17, 18)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [maria, petya, stoyan])

        result_set = User.select().where(User.name.startswith('M')).get()
        self.assertEqual(next(result_set), maria)

        result_set = User.select().where(User.name.endswith('a')).first()
        self.assertEqual(result_set, maria)

        result_set = User.select().where(User.name.contains('y')).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [stoyan, petya])

        result_set = User.select().where(User.age >= 50).first()
        self.assertIsNone(result_set)

        result_set = User.select().where(
            to_lowercase(User.name) == 'ivan').get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [ivan, ivan_])

    def test_combine(self):
        result_set = User.select().where(
            or_(User.name == 'Ivan', User.age > 10)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, self.users)

        result_set = User.select().where(
            and_(User.name == 'Ivan', User.age == 20)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [ivan])

        result_set = User.select(User.name, User.age).where(
            or_(User.name == 'Ivan', User.age > 10)).get()
        result_set = [user for user in result_set]
        # could also return objects
        self.assertListEqual(
            result_set, [(user.name, user.age) for user in self.users])

    def test_limit(self):
        result_set = User.select().where(User.is_active).limit(2).get()
        result_set = [user for user in result_set]
        self.assertEqual(len(result_set), 2)

        result_set = User.select().where(User.age == 18).limit(4).get()
        result_set = [user for user in result_set]
        self.assertEqual(len(result_set), 2)
        self.assertListEqual(result_set, [stoyan, maria])


if __name__ == '__main__':
    unittest.main()
