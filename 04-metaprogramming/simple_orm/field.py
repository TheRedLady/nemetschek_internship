from query import Query


def or_(left, right):
    left = Query(lhs=left['lhs'], operator=left['operator'], rhs=left['rhs'])
    right = Query(lhs=right['lhs'], operator=right['operator'], rhs=right['rhs'])
    return make_expression(None, left, ' OR ', right)


def and_(left, right):
    left = Query(lhs=left['lhs'], operator=left['operator'], rhs=left['rhs'])
    right = Query(lhs=right['lhs'], operator=right['operator'], rhs=right['rhs'])
    return make_expression(None, left, ' AND ', right)


def make_expression(field, lhs, operator, rhs):
    if hasattr(field, 'lhs'):
        lhs = field.lhs
    expr = {'lhs': lhs, 'operator': operator, 'rhs': rhs}
    return expr


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
        return make_expression(self, self.name, ' = ', other)

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.value != other.value
        return make_expression(self, 'NOT ' + self.name, ' = ', other)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return make_expression(self, self.name, ' < ', other)

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        return make_expression(self, self.name, ' <= ', other)

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        return make_expression(self, self.name, ' > ', other)

    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.value >= other.value
        return make_expression(self, self.name, ' >= ', other)

    def in_(self, *values):
        return make_expression(self, self.name, ' IN ', list(values))

    def startswith(self, value):
        value = value + "%"
        return make_expression(self, self.name, ' LIKE ', value)

    def endswith(self, value):
        value = "%" + value
        return make_expression(self, self.name, ' LIKE ', value)

    def contains(self, substring):
        substring = "%" + substring + "%"
        return make_expression(self, self.name, ' LIKE ', substring)


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



