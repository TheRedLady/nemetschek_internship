from field import Field, AutoField
from query import Query


class ModelMetaclass(type):
    # store fields in class
    # keep track of definition sequence

    def __new__(metaclass, classname, bases, class_dict):
        columns = []
        for name, value in class_dict.items():
            if isinstance(value, Field):
                value.name = name
                columns.append((value.creation_counter, value))
        if 'database' not in class_dict:
            raise AttributeError("DB not provided")
        for parent in bases:
            if isinstance(parent, ModelMetaclass):
                columns.extend(parent.fields)
        columns.sort()
        class_dict['fields'] = columns
        class_dict['table_name'] = '"' + classname.lower() + '"'
        return type.__new__(metaclass, classname, bases, class_dict)


class Model(object):

    __metaclass__ = ModelMetaclass

    id = AutoField(primary_key=True)

    database = None

    @classmethod
    def row_to_object(cls, row):
        if row is None:
            return row
        fields = [field.name for field in cls.columns]
        obj_dict = dict(zip(fields, row))
        obj = object.__new__(cls)
        cls.__init__(obj, **obj_dict)
        return obj

    @classmethod
    def select(cls, *args):
        args = [a.name for a in args]
        Query.class_ = cls
        Query.db_type = cls.database.db_type
        return Query(defered_fields=args)

    @classmethod
    def filter(cls, expr):
        query = cls.select().where(expr)
        query_set = query.get()
        query_set = [cls.row_to_object(row) for row in query_set]
        return query_set

    @classmethod
    def setup_schema(cls):
        cls.columns = [field[1] for field in cls.fields]
        Field.db_type = cls.database.db_type
        cls.database.create_table(cls)

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name + '_', value)

    def __eq__(self, other):
        if other is None:
            return False
        return self.id_ == other.id_

    def insert(self):
        self.database.insert_table(self)
        self.id_ = self.database.lastrow_id

    def update(self):
        self.database.update_table(self)

    def save(self):
        if hasattr(self, 'id_'):
            self.update()
        else:
            self.insert()
