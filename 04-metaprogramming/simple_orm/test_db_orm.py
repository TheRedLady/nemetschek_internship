import unittest
import collections
import sqlite3

import cursor
import query
import field as field
import simple_orm as model


db = cursor.Cursor('sqlite')


class User(model.Model):

    name = field.CharField()
    age = field.IntField()
    is_active = field.BooleanField()

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
        User.setup_schema()
        self.users = [ivan, ivan_, maria, petya, lili, todor, biser, stoyan,
                      nikol]
        for user in self.users:
            user.save()

    def tearDown(self):
        db.cursor.execute('DROP TABLE user')

    def test_get(self):
        result_set = User.select().where(User.is_active == True).get()
        self.assertIsInstance(result_set, collections.Iterable)
        self.assertIn(next(result_set), self.users)

        result_set = User.select().where(User.is_active == True).where(
            User.age < 25).where(User.name.startswith('S')).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [stoyan])

        self.assertIsNone(next(User.select().where(User.name == 'Georgi').get()))

        result_set = User.select().where(User.age.in_(17, 18)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [maria, petya, stoyan])

        result_set = User.select().where(User.name.startswith('M')).get()
        self.assertEqual(next(result_set), maria)

        result_set = User.select().where(User.name.contains('y')).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [stoyan, petya])

    def test_one(self):
        result_set = User.select().where(User.name == 'Lili').one()
        self.assertEqual(result_set, lili)

        result_set = User.select().where(User.age == 17).one()
        self.assertEqual(result_set, petya)

        with self.assertRaises(query.MultipleResultsError):
            User.select().where(User.name == 'Ivan').one()

    def test_first(self):
        result_set = User.select().where(User.name.endswith('a')).first()
        self.assertEqual(result_set, maria)

        result_set = User.select().where(User.is_active == True).first()
        self.assertEqual(result_set, lili)

        result_set = User.select().where(User.age >= 50).first()
        self.assertIsNone(result_set)

    def test_or(self):
        result_set = User.select().where(
            field.or_(User.name == 'Ivan', User.age > 10)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, self.users)

        result_set = User.select().where(
            field.or_(User.name.contains('i'), User.age < 20)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [ivan, ivan_, nikol, maria, biser, lili, petya, stoyan])

        result_set = User.select(User.name, User.age).where(
            field.or_(User.name == 'Ivan', User.age > 10)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(
            result_set, [(user.name, user.age) for user in self.users])

    def test_and(self):
        result_set = User.select().where(
           field.and_(User.name == 'Ivan', User.age == 20)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [ivan])

        result_set = User.select().where(
           field.and_(User.is_active == True, User.age < 20)).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [maria, stoyan])

        result_set = User.select(User.name, User.is_active).where(
           field.and_(User.is_active == False, User.name.endswith('a'))).get()
        result_set = [user for user in result_set]
        self.assertListEqual(result_set, [(petya.name, petya.is_active)])

    def test_limit(self):
        result_set = User.select().where(User.is_active == True).limit(2).get()
        result_set = [user for user in result_set]
        self.assertEqual(len(result_set), 2)

        result_set = User.select().where(User.age == 18).limit(4).get()
        result_set = [user for user in result_set]
        self.assertEqual(len(result_set), 2)
        self.assertListEqual(result_set, [stoyan, maria])


if __name__ == '__main__':
    unittest.main()
