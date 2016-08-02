import collections


def wrap_sequence(iterable):
    if len(iterable) == 1:
        return "(" + str(iterable[0]) + ")"
    iterable = [str(i) for i in iterable]
    st = ", ".join(iterable)
    return "(" + st + ")"


def wrap_values(length):
    if length == 1:
        return '?'
    st = length * ['?']
    st = ', '.join(st)
    return '(' + st + ')'


class MultipleResultsError(Exception):
    pass


class Query(object):

    def __init__(self, class_=None, defered_fields=None, lhs=None,
                 rhs=None, operator=None):
        self.class_ = class_
        self.values = []
        if defered_fields:
            self.defered = ', '.join(defered_fields)
        else:
            self.defered = '*'
        self.lhs = lhs
        self.operator = operator
        rhs = self.type_check(rhs)
        self.rhs = rhs
        self.append_values(self.rhs)

    def type_check(self, value):
        if self.class_ is not None:
            if value in (True, False) and self.class_.Meta.database.types['BooleanField'] == 'INTEGER':
                return 1 if value else 0
        return value

    def to_sql(self):
        if isinstance(self.lhs, Query):
            self.lhs = self.lhs.to_sql()
        else:
            self.lhs = str(self.lhs) if self.lhs is not None else ''
        if isinstance(self.rhs, Query):
            self.rhs = self.rhs.to_sql()
        else:
            if isinstance(self.rhs, list):
                self.rhs = wrap_values(len(self.rhs))
            elif self.rhs in self.values:
                self.rhs = '?'
            else:
                self.rhs = str(self.rhs) if self.rhs is not None else ''
        if self.operator is None:
            self.operator = ''
        return self.lhs + self.operator + self.rhs

    def append_values(self, other):
        if other is None:
            return
        elif isinstance(other, Query):
            self.values.extend(other.values)
        elif isinstance(other, collections.Iterable) and not isinstance(other, str):
            self.values.extend(other)
        else:
            self.values.append(other)

    def where(self, kwargs):
        lhs = kwargs['lhs']
        rhs = kwargs['rhs']
        operator = kwargs['operator']
        if self.lhs is None:
            self.lhs = lhs
            self.operator = operator
            self.rhs = self.type_check(rhs)
            if isinstance(self.lhs, Query):
                self.append_values(self.lhs)
            self.append_values(self.rhs)
        else:
            self.lhs = Query(class_=self.class_, lhs=self.lhs,
                             operator=self.operator, rhs=self.rhs)
            self.rhs = Query(class_=self.class_, lhs=lhs,
                             operator=operator, rhs=rhs)
            self.operator = ' AND '
            self.append_values(self.rhs)
        return self

    def limit(self, lim):
        self.lhs = Query(class_=self.class_, lhs=self.lhs,
                         operator=self.operator, rhs=self.rhs)
        self.rhs = '?'
        self.operator = ' LIMIT '
        self.values.append(lim)
        return self

    def prepare_select(self):
        query = 'SELECT {} FROM {} WHERE '.format(self.defered, self.class_.table_name)
        query += self.to_sql()
        self.return_object = False if self.defered != '*' else True
        return query, tuple(self.values)

    def get(self):
        cursor = self.class_.Meta.database.cursor
        cursor.execute(*self.prepare_select())
        row = cursor.fetchone()
        if row is None:
            yield row
        while row is not None:
            if self.return_object:
                yield self.class_.row_to_object(row)
            else:
                yield row
            row = cursor.fetchone()

    def one(self):
        cursor = self.class_.Meta.database.cursor
        cursor.execute(*self.prepare_select())
        row = cursor.fetchone()
        if self.return_object:
            row = self.class_.row_to_object(row)
        if cursor.fetchone() is not None:
            raise MultipleResultsError
        return row

    def first(self):
        cursor = self.class_.Meta.database.cursor
        cursor.execute(*self.prepare_select())
        row = cursor.fetchone()
        if self.return_object:
            row = self.class_.row_to_object(row)
        return row

