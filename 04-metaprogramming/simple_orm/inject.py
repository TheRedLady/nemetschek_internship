

class Injected(object):

    injected_value = None
    injected = {}

    @classmethod
    def inject(cls, **injected):
        for name, value in injected.iteritems():
            for field in cls.injected.get(name, []):
                field.injected_value = value

    def __init__(self, service_name):
        self.service_name = service_name
        Injected.injected.setdefault(service_name, []).append(self)

    def __get__(self, obj, type=None):
        if obj is None and type is None:
            return self
        if self.injected_value is None:
            raise Exception('Not injected yet')
        return self.injected_value

    def __set__(self, obj, val):
        raise Exception('Cannot set injectable')

