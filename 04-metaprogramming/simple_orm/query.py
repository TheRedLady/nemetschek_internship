import collections


def wrap_sequence(iterable):
    iterable = [str(i) for i in iterable]
    st = ', '.join(iterable)
    return '(' + st + ')'


def wrap_dict_colon(names):
    dict_names = [':' + str(name) for name in names]
    dict_names = ', '.join(dict_names)
    return '(' + dict_names + ')'


def wrap_dict_percent(names):
    dict_names = ['%(' + str(name) + ')s' for name in names]
    dict_names = ', '.join(dict_names)
    return '(' + dict_names + ')'


def wrap_values_question_marks(length):
    if length == 1:
        return '?'
    st = length * ['?']
    st = ', '.join(st)
    return '(' + st + ')'


def wrap_values_percent(length):
    if length == 1:
        return "%s"
    st = length * ["%s"]
    st = ', '.join(st)
    return '(' + st + ')'


wrap_values = {'sqlite': wrap_values_question_marks, 'postgre': wrap_values_percent,
               'mysql': wrap_values_percent}
wrap_dict = {'sqlite': wrap_dict_colon, 'postgre': wrap_dict_percent,
             'mysql': wrap_dict_percent}


class MultipleResultsError(Exception):
    pass


class Query(object):

    db_type = ''

    def __init__(self, defered_fields=None, lhs=None, rhs=None, operator=None):
        self.values = []
        if defered_fields:
            self.defered = ', '.join(defered_fields)
        else:
            self.defered = '*'
        self.lhs = lhs
        if isinstance(self.lhs, Query):
            self.append_values(self.lhs)
        self.operator = operator
        self.rhs = rhs
        self.append_values(self.rhs)

    def to_sql(self):
        if isinstance(self.lhs, Query):
            self.lhs = self.lhs.to_sql()
        else:
            self.lhs = str(self.lhs) if self.lhs is not None else ''
        if isinstance(self.rhs, Query):
            self.rhs = self.rhs.to_sql()
        else:
            if isinstance(self.rhs, list):
                self.rhs = wrap_values[self.db_type](len(self.rhs))
            elif self.rhs in self.values:
                self.rhs = wrap_values[self.db_type](len([self.rhs]))
            else:
                self.rhs = str(self.rhs) if self.rhs is not None else ''
        if self.operator is None:
            self.operator = ''
        return self.lhs + self.operator + self.rhs

    def append_values(self, other):
        if other is None:
            return
        if isinstance(other, Query):
            self.values.extend(other.values)
        elif isinstance(other, collections.Iterable) and not isinstance(other, str):
            self.values.extend(other)
        else:
            self.values.append(other)

    def where(self, query):
        query.defered = self.defered
        self = query
        return self

    def limit(self, lim):
        self = Query(defered_fields=self.defered, lhs=self, operator=' LIMIT ',
                     rhs=lim)
        return self

    def prepare_select(self):
        query = 'SELECT {} FROM {}'.format(self.defered, self.class_.table_name)
        if self.values:
            query += ' WHERE '
        query += self.to_sql()
        self.return_object = False if self.defered != '*' else True
        return query, tuple(self.values)

    def get(self):
        cursor = self.class_.database.cursor
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
        cursor = self.class_.database.cursor
        cursor.execute(*self.prepare_select())
        row = cursor.fetchone()
        if self.return_object:
            row = self.class_.row_to_object(row)
        if cursor.fetchone() is not None:
            raise MultipleResultsError
        return row

    def first(self):
        cursor = self.class_.database.cursor
        cursor.execute(*self.prepare_select())
        row = cursor.fetchone()
        if self.return_object:
            row = self.class_.row_to_object(row)
        return row

