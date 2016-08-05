from query import Query
import copy


data_types = {'sqlite': {'IntField': 'INTEGER', 'CharField': 'TEXT',
                         'BooleanField': 'INTEGER',
                         'AutoField': 'INTEGER PRIMARY KEY'},
              'postgre': {'IntField': 'INTEGER', 'CharField': 'TEXT',
                          'BooleanField': 'BOOLEAN', 'AutoField': 'Serial'}}

func_types = {'sqlite': {'to_lowercase': 'LOWER', 'to_uppercase': 'UPPER',
                         'max': 'MAX', 'avg': 'AVG'},
              'postgre': {'to_lowercase': 'LOWER', 'to_uppercase': 'UPPER',
                          'max': 'MAX', 'avg': 'AVG'}}


def dbfunc(db_type):
    def wrapper(func):
        def decorator(field):
            new_field = copy.copy(field)
            new_field.name = func_types[db_type][func.__name__] + "(" + field.name + ")"
            return func(new_field)
        return decorator
    return wrapper


def or_(*args):
    if len(args) == 2:
        return Query(lhs=args[0], rhs=args[1], operator=' OR ')
    return Query(lhs=args[0], rhs=or_(*args[1::]), operator=' OR ')


def and_(*args):
    if len(args) == 2:
        return Query(lhs=args[0], rhs=args[1], operator=' AND ')
    return Query(lhs=args[0], rhs=and_(*args[1::]), operator=' AND ')


class ValidationError(Exception):
    pass


class Field(object):

    db_type = None

    creation_counter = 1

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
        return Query(lhs=self.name, operator=' = ', rhs=other)

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.value != other.value
        return Query(lhs='NOT ' + self.name, operator=' = ', rhs=other)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return Query(lhs=self.name, operator=' < ', rhs=other)

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        return Query(lhs=self.name, operator=' <= ', rhs=other)

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        return Query(lhs=self.name, operator=' > ', rhs=other)

    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.value >= other.value
        return Query(lhs=self.name, operator=' >= ', rhs=other)

    def in_(self, *values):
        return Query(lhs=self.name, operator=' IN ', rhs=list(values))

    def startswith(self, value):
        value = value + "%"
        return Query(lhs=self.name, operator=' LIKE ', rhs=value)

    def endswith(self, value):
        value = "%" + value
        return Query(lhs=self.name, operator=' LIKE ', rhs=value)

    def contains(self, substring):
        substring = "%" + substring + "%"
        return Query(lhs=self.name, operator=' LIKE ', rhs=substring)

    @property
    def db_field_type(self):
        return data_types[self.db_type][self.__class__.__name__]


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

