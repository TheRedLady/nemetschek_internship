import numbers

"""
@validate(
    arg('x', [number, lambda x: 0 < x]),
    arg('y', [instance(Iterable)]),
)
def calc(x, y):
    pass
"""


def is_number(n):
    return is_instanceof(numbers.Number)(n)  # return isinstance(n, numbers.Number)


def is_string(n):
    return is_instanceof(str)(n)  # return isinstance(n, str)


def is_instanceof(type):
    return lambda arg: isinstance(arg, type)


def arg(name, validators):
    def func_validate(arg_dict):
        for val in validators:
            if not val(arg_dict[name]):
                return False
        return True
    return func_validate


def validate(*validators):
    def decorator(f):
        def check(*args):
            arg_dict = f.__code__.co_varnames
            arg_dict = {name: value for name, value in zip(arg_dict, args)}
            for item in validators:
                if not item(arg_dict):
                    raise TypeError("Invalid arguments")
            return f(*args)
        return check
    return decorator
