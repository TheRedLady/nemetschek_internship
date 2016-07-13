class Field(object):
    def __init__(self):
        pass

    def __get__(self, obj, type=None):
        pass

    def __set__(self, obj, value):
        pass


class IntField(Field):
    pass


class CharField(Field):
    pass


class ModelMetaclass(type):

    def __new__(metaclass, classname, bases, class_dict):
        pass


class Model(object):

    __metaclass__ = ModelMetaclass

    id = IntField()
    id.db_type = 'INTEGER PRIMARY KEY AUTOINCREMENT'

    @classmethod
    def setup_schema(cls, cursor):
        pass

    def __init__(self, cursor, **kwargs):
        pass

    def save(self):
        pass
