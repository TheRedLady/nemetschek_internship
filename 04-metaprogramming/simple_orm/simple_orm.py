import collections
import cursor

class ValidationError(Exception):
    pass


class MultipleResultsError(Exception):
    pass


def or_(left, right):
    left = cursor.Query(lhs=left['lhs'], operator=left['operator'], rhs=left['rhs'])
    right = cursor.Query(lhs=right['lhs'], operator=right['operator'], rhs=right['rhs'])
    return {'lhs': left, 'operator': ' OR ', 'rhs': right}


def and_(left, right):
    left = cursor.Query(lhs=left['lhs'], operator=left['operator'], rhs=left['rhs'])
    right = cursor.Query(lhs=right['lhs'], operator=right['operator'], rhs=right['rhs'])
    return {'lhs': left, 'operator': ' AND ', 'rhs': right}



class Field(object):

    creation_counter = 1
    autocreation_counter = 0

    def __init__(self, name=None, primary_key=False, null=True,
                 default=None, value=None):
        self.name = name
        self.primary_key = primary_key
        self.null = null
        self.value = value
        self.default = default
        if self.value is None and self.default is not None:
            self.value = default
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def validate(self, value):
        pass

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            if hasattr(obj, self.name + '_'):
                return getattr(obj, self.name + '_')
            else:
                raise AttributeError

    def __set__(self, obj, value):
        self.validate(value)
        if obj is not None:
            setattr(obj, self.name + '_', value)
        else:
            self.value = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        return {'lhs': self.name, 'operator': '=', 'rhs': other}

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.value != other.value
        return {'lhs': 'NOT ' + self.name, 'operator': '=', 'rhs': other}

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return {'lhs': self.name, 'operator': ' < ', 'rhs': other}

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return {'lhs': self.name, 'operator': ' > ', 'rhs': other}

    def in_(self, *values):
        return {'lhs': self.name, 'operator': ' IN ', 'rhs' : list(values)}

    def startswith(self, value):
        value =  value + "%"
        return {'lhs': self.name, 'operator': ' LIKE ', 'rhs': value}

    def endswith(self, value):
        value =  "%" + value
        return {'lhs': self.name, 'operator': ' LIKE ', 'rhs': value}



class IntField(Field):

    def validate(self, value):
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError
        if value is not None and not isinstance(value, int):
            raise ValidationError


class CharField(Field):

    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super(CharField, self).__init__(**kwargs)

    def validate(self, value):
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError
        if not isinstance(value, str):
            raise ValidationError
        if self.max_length and len(value) > self.max_length:
            raise ValidationError
        if self.min_length and len(value) < self.min_length:
            raise ValidationError



class BooleanField(Field):

    def validate(self, value):
        if value is None:
            if self.primary_key or not self.null:
                raise ValidationError
        if value not in (True, False, 0, 1):
            raise ValidationError

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return bool(getattr(obj, self.name + '_'))

    def __set__(self, obj, value):
        self.validate(value)
        if obj is not None:
            setattr(obj, self.name + '_', value)
        else:
            self.value = value


class AutoField(IntField):
    pass


class ModelMetaclass(type):
    # store fields in class
    # keep track of definition sequence

    def __new__(metaclass, classname, bases, class_dict):
        columns = []
        for name, value in class_dict.items():
            if isinstance(value, Field):
                value.name = name
                columns.append((value.creation_counter, value))
        if 'Meta' not in class_dict:
            raise AttributeError("Class 'Meta' not provided")
        for parent in bases:
            if isinstance(parent, ModelMetaclass):
                columns.extend(parent.fields)
        columns.sort()
        class_dict['fields'] = columns
        class_dict['table_name'] = classname.lower()
        return type.__new__(metaclass, classname, bases, class_dict)


class Model(object):

    __metaclass__ = ModelMetaclass

    id = AutoField(primary_key=True)

    class Meta:
        database = None

    @classmethod
    def row_to_object(cls, row):
        if row is None:
            return row
        fields = [field.name for field in cls.columns]
        obj_dict = dict(zip(fields, row))
        return cls.__new__(cls, obj_dict)

    @classmethod
    def select(cls, *args):
        args = [a.name for a in args]
        return cursor.Query(cls, args)

    @classmethod
    def filter(cls, condition):
        query = cls.select().where(*condition).to_sql()
        query_set = cls.Meta.database.cursor.fetchall(*query)
        query_set = [cls.row_to_object(row) for row in query_set]
        return query_set

    @classmethod
    def setup_schema(cls):
        cls.columns = [field[1] for field in cls.fields]
        cls.Meta.database.create_table(cls)

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if value in (True, False) and self.Meta.database.types['BooleanField'] == 'INTEGER':
                value = 1 if value else 0
            setattr(self, name + '_', value)

    def __eq__(self, other):
        return list(set(self.columns).intersection(other.columns)) == self.columns

    def insert(self):
        self.Meta.database.insert_table(self)

    def update(self):
        self.Meta.database.update_table(self)

    def save(self):
        if hasattr(self, 'id_'):
            self.update()
        else:
            self.insert()
