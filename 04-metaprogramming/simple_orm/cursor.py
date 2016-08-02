import sqlite3
import psycopg2
from field import BooleanField


class UnsupportedDBMSError(Exception):
    pass


class Cursor(object):

    data_types = {'sqlite': {'IntField': 'INTEGER', 'CharField': 'TEXT',
                             'BooleanField': 'INTEGER',
                             'AutoField': 'INTEGER PRIMARY KEY'},
                  'postgre': {'IntField': 'INTEGER', 'CharField': 'TEXT',
                              'BooleanField': 'BOOLEAN', 'AutoField': 'Serial'}}

    def __init__(self, db_type, dsn=None, user=None, password=None,
                 host=None, database=None):
        if db_type not in self.data_types:
            raise UnsupportedDBMSError
        if db_type == 'sqlite':
            if dsn is None:
                dsn = ':memory:'
            self.connection = sqlite3.connect(dsn)
        else:
            self.connection = psycopg2.connect(database=database, user=user,
                                               password=password, host=host)
        self.cursor = self.connection.cursor()
        self.prepare(db_type)

    def prepare(self, db_type):
        self.types = self.data_types[db_type]

    def create_table(self, class_):
        query = ''
        for c in class_.columns:
            if query:
                query += ', '
            query += c.name + ' ' + self.types[c.__class__.__name__]
        query = 'CREATE TABLE {} ({})'.format(class_.table_name, query)
        self.cursor.execute(query)

    def update_table(self, obj):
        query = 'UPDATE {} SET '.format(obj.table_name)
        for field in obj.columns:
            self.cursor.execute(query + field.name + ' = :' + field.name + ' WHERE id = :id',
            {field.name: getattr(obj, field.name + '_'), 'id': obj.id_})

    def insert_table(self, obj):
        query = 'INSERT INTO {} '.format(obj.table_name)
        field_names = []
        values_dict = {}
        for field in obj.columns:
            if field.name == 'id':
                continue
            field_names.append(field.name)
            value = getattr(obj, field.name + '_')
            if isinstance(field, BooleanField) and self.types['BooleanField'] == 'INTEGER':
                value = 1 if value else 0
            values_dict[field.name] = value
        if len(field_names) > 1:
            query += '(' + ', '.join(field_names) + ')'
            field_names = '(' + ', '.join([':' + name for name in field_names]) + ')'
        else:
            field_names = field_names.pop()
            query += '(' + field_names + ')'
            field_names = '(:' + field_names[0] + ')'
        self.cursor.execute(query + ' VALUES ' + field_names, values_dict)

