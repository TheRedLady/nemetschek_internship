from collections import defaultdict


def wrap(txt):
    return '"' + txt + '"'


class ValidationError(Exception):
    pass


class Field(object):

    creation_counter = 1
    autocreation_counter = 0
    db_type = ''

    def __init__(self, name=None, primary_key=False, max_length=None, null=True,
                 default=None, autoincrement=False, value=None):
        self.name = name
        self.primary_key = primary_key
        self.value = value
        if self.primary_key:
            self.db_type += ' PRIMARY KEY'
        if autoincrement:
            self.db_type += ' AUTOINCREMENT'
            self.value = Field.autocreation_counter
            Field.autocreation_counter += 1
        self.max_length = max_length
        self.null = null
        self.default = default
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if self.value is None and self.default:
            return self.default
        return self.value

    def validate(self, value):
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError

    def __set__(self, obj, value):
        self.validate(value)
        self.value = value

    def __eq__(self, value):
        if isinstance(value, str):
            value = wrap(value)
        return self.name + ' = :' + self.name, {self.name: value}

    def __ne__(self, value):
        if isinstance(value, str):
            value = wrap(value)
        return 'NOT ' + self.name + ' = :' + self.name, {self.name: value}

    @classmethod
    def or_(cls, fst, snd):
        values = []
        key, value = fst[1].popitem()
        values.append(value)
        key, value = snd[1].popitem()
        values.append(value)
        return key + " = ?" + " OR " + key + " = ?", tuple(values)

    def startswith(self, val):
        return self.name + ' LIKE ":name%"', {self.name: val}


class IntField(Field):
    db_type = 'INTEGER'

    def validate(self, value):
        if value is not None and not isinstance(value, int):
            raise ValidationError
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError


class CharField(Field):
    db_type = 'TEXT'

    def validate(self, value):
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError
        if not isinstance(value, str):
            raise ValidationError
        if self.max_length and len(value) > self.max_length:
            raise ValidationError


class ModelMetaclass(type):
    # store fields in class
    # keep track of definition sequence

    def __new__(metaclass, classname, bases, class_dict):
        columns = []
        for name, value in class_dict.items():
            if isinstance(value, Field):
                value.name = name
                columns.append((value.creation_counter, value))
        for parent in bases:
            if isinstance(parent, ModelMetaclass):
                columns.extend(parent.fields)
        columns.sort()
        class_dict['fields'] = columns
        class_dict['table_name'] = classname.lower()
        return type.__new__(metaclass, classname, bases, class_dict)


class Model(object):

    __metaclass__ = ModelMetaclass

    id = IntField(autoincrement=True, primary_key=True)

    @classmethod
    def filter(cls, cursor, sub):
        query = 'SELECT * FROM {} WHERE '.format(cls.table_name)
        cursor.execute(query + sub[0], sub[1])

    @classmethod
    def setup_schema(cls, cursor):
        fields = ''
        for col in cls.fields:
            if fields:
                fields += ', '
            fields += col[1].name + ' ' + col[1].db_type
        query = 'CREATE TABLE {} ({})'.format(cls.table_name, fields)
        cursor.execute(query)

    def __init__(self, cursor, **kwargs):
        self.cursor = cursor
        for name, value in kwargs.items():
            setattr(self, name, value)

    def insert(self):
        query = 'INSERT INTO {}'.format(self.table_name)
        for field in self.fields:
            self.cursor.execute(
                query +
                ' (' + field[1].name + ') VALUES (:' + field[1].name + ')',
                {field[1].name: field[1].value})

    def update(self):
        query = 'UPDATE {} SET '.format(self.table_name)
        for field in self.fields:
            self.cursor.execute(
                query + field[1].name + ' = :' + field[1].name + ' WHERE id = :id',
                {field[1].name: field[1].value, 'id': self.id})

    def save(self):
        if self.id:
            self.update()
        else:
            self.insert()
