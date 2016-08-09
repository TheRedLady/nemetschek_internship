from query import Query
import copy


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
            elif self.default is not None:
                return self.default
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

    '''
    @property
    def db_field_type(self):
        type_ = data_types[self.db_type][self.__class__.__name__]
        if self.primary_key:
            if not (self.db_type == 'sqlite' and isinstance(self, AutoField)):
                type_ += ' PRIMARY KEY'
        if not self.null:
            type_ += ' NOT NULL'
        if self.default is not None:
            type_ += ' DEFAULT {}'.format(self.default)
        return type_
    '''


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
        if hasattr(obj, self.name + '_'):
            return bool(getattr(obj, self.name + '_'))
        if self.default is not None:
            return self.default
        else:
            raise AttributeError

    def __set__(self, obj, value):
        self.validate(value)
        if obj is not None:
            setattr(obj, self.name + '_', value)
        else:
            self.value = value


class AutoField(IntField):
    pass

