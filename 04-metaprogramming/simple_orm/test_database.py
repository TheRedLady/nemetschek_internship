import unittest
import mock

import database
import field
import model


class MockDatabase(database.Database):

    data_types = {'IntField': 'INTEGER', 'CharField': 'TEXT',
                  'BooleanField': 'INTEGER', 'AutoField': 'INTEGER'}

    def __init__(self, cursor):
        self.cursor = cursor

    def type_check(self, value):
        if value is True or value is False:
            return 1 if value else 0
        return value


db = MockDatabase(mock.Mock())


class Pony(model.Model):
    database = db
    color = field.CharField()
    age = field.IntField()


class TestDB(unittest.TestCase):

    def test_setup(self):
        db.create_table(Pony)
        db.cursor.execute.assert_called_with(
            'CREATE TABLE pony (id INTEGER PRIMARY KEY, color TEXT, age INTEGER)')

    def test_insert(self):
        my_little_pony = Pony(color='pink', age=11)
        db.insert_table(my_little_pony)
        db.cursor.execute.assert_called_with(
            'INSERT INTO pony (color, age) VALUES (:color, :age)',
            {'color': 'pink', 'age': 11})

    def test_update(self):
        my_little_pony = Pony(color='pink', age=9, id=1)
        db.update_table(my_little_pony)
        db.cursor.execute.assert_called_with(
            'UPDATE pony SET age = :age WHERE id = :id',
            {'age': 9, 'id': 1})


if __name__ == '__main__':
    unittest.main()
