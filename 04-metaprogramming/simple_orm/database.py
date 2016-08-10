import copy


def wrap_sequence(iterable):
    iterable = [str(i) for i in iterable]
    st = ', '.join(iterable)
    return '(' + st + ')'


def dbfunc(db_type):
    def wrapper(func):
        def dec(field):
            new_field = copy.copy(field)
            new_field.name = func(field)
            return new_field
        return dec
    return wrapper


class UnsupportedDBMSError(Exception):
    pass


class Database(object):

    data_types = {}
    placeholder = '?'

    def __init__(self, **connection_parameters):
        pass

    def _assemble_field_type(self, field):
        type_ = self.data_types[field.__class__.__name__]
        if field.primary_key:
            type_ += ' PRIMARY KEY'
        if not field.null:
            type_ += ' NOT NULL'
        if field.default is not None:
            type_ += ' DEFAULT {}'.format(field.default)
        return type_

    def table_name(self, table_name):
        return table_name

    def type_check(self, value):
        return value

    def wrap_dict(self, names):
        if len(names) == 1:
            return ':' + names[0]
        dict_names = [':' + str(name) for name in names]
        dict_names = ', '.join(dict_names)
        return '(' + dict_names + ')'

    def wrap_values(self, length):
        if length == 1:
            return self.placeholder
        st = length * [self.placeholder]
        st = ', '.join(st)
        return '(' + st + ')'

    def create_table(self, class_):
        query = ''
        for c in class_.columns:
            if query:
                query += ', '
            query += c.name + ' ' + self._assemble_field_type(c)
        query = 'CREATE TABLE {} ({})'.format(self.table_name(class_.table_name), query)
        self.cursor.execute(query)

    def update_table(self, obj):
        query = 'UPDATE {} SET '.format(self.table_name(obj.table_name))
        for field in obj.columns:
            self.cursor.execute(query + field.name + ' = ' + self.wrap_dict([field.name]) + ' WHERE id = :id',
            {field.name: self.type_check(getattr(obj, field.name + '_')), 'id': obj.id_})

    def insert_table(self, obj):
        query = 'INSERT INTO {} '.format(self.table_name(obj.table_name))
        field_names = []
        values_dict = {}
        for field in obj.columns:
            if field.name == 'id':
                continue
            field_names.append(field.name)
            value = getattr(obj, field.name + '_')
            values_dict[field.name] = self.type_check(value)
        query += wrap_sequence(field_names)
        field_names = self.wrap_dict(field_names)
        self.cursor.execute(query + ' VALUES ' + field_names, values_dict)

    @property
    def lastrow_id(self):
        return self.cursor.lastrowid
