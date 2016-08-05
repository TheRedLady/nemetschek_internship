import sqlite3
import psycopg2
from field import BooleanField
from query import wrap_dict, wrap_sequence


class UnsupportedDBMSError(Exception):
    pass


class Cursor(object):

    db_types = ['postgre', 'sqlite']

    def __init__(self, db_type, dsn=None, user=None, password=None, port=None,
                 host=None, database=None):
        if db_type not in self.db_types:
            raise UnsupportedDBMSError
        if db_type == 'sqlite':
            if dsn is None:
                dsn = ':memory:'
            self.connection = sqlite3.connect(dsn)
        else:
            self.connection = psycopg2.connect(database=database, user=user,
                                               port=port, password=password, host=host)
        self.db_type = db_type
        self.cursor = self.connection.cursor()

    def create_table(self, class_):
        query = ''
        for c in class_.columns:
            if query:
                query += ', '
            query += c.name + ' ' + c.db_field_type
        query = 'CREATE TABLE {} ({})'.format(class_.table_name, query)
        self.cursor.execute(query)

    def update_table(self, obj):
        query = 'UPDATE {} SET '.format(obj.table_name)
        for field in obj.columns:
            self.cursor.execute(query + field.name + ' = ' + wrap_dict[self.db_type](field.name) + ' WHERE id = :id',
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
            values_dict[field.name] = value
        query += wrap_sequence(field_names)
        field_names = wrap_dict[self.db_type](field_names)
        self.cursor.execute(query + ' VALUES ' + field_names, values_dict)

    @property
    def lastrow_id(self):
        if self.db_type == 'postgre':
            self.cursor.execute('select lastval()')
            id = self.cursor.fetchone()[0]
        else:
            id = self.cursor.lastrowid
        return id

