"""
@validate(
    arg('x', [number, lambda x: 0 < x]),
    arg('y', [instance(Iterable)]),
)
def calc(x, y):
    pass
"""


def is_number(n):
    pass


def is_string(n):
    pass


def is_instanceof(type):
    pass


def arg(name, validators):
    pass


def validate(validators):
    pass
