class Pred(object):

    def __init__(self, f):
        self.func = f

    def __call__(self, *args):
        return self.func(*args)

    def __and__(self, other):
        return Pred(lambda x: self(x) and other(x))

    def __or__(self, other):
        return Pred(lambda x: self(x) or other(x))

    def __rshift__(self, other):
        return Pred(lambda x: self(x) or other(x))

    def __invert__(self):
        return Pred(lambda x: not self(x))

def gt(x):
    return Pred(lambda y: x < y)

def lt(x):
    return Pred(lambda y: x > y)

def eq(x):
    return Pred(lambda y: x == y)

def oftype(t):
    return Pred(lambda y: isinstance(y, t))

def present():
    return Pred(lambda y: y is not None)


def for_any(*predicates):
    def check_pr(arg):
        for pred in predicates:
            if pred(arg):
                return True
        return False
    return Pred(check_pr)


def for_all(*predicates):
    def check_pr(arg):
        for pred in predicates:
            if not pred(arg):
                return False
        return True
    return Pred(check_pr)
