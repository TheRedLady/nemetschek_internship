import operator

def wrap(f):
    def wrapper(*args):
        return create(f.func_name, *args) 
    return wrapper

def create(op, *args):
    result = Lazy(args[0])
    result.rhs = args[1] 
    result.op = getattr(operator, op)
    return result

#STR_REPR = { "__add__":"+", "__sub":"-" }


class Lazy:

    def __init__(self, number):
        self.lhs = number
        self.op = None
        self.rhs = None
        self.sign = None
        
    def force(self):
        if self.lhs and isinstance(self.lhs, Lazy):
            self.lhs = self.lhs.force()
        if self.rhs and isinstance(self.rhs, Lazy):
            self.rhs = self.rhs.force()
        if self.sign:
            self.lhs = self.sign(self.lhs)
        if self.op: 
            return self.op(self.lhs, self.rhs)
        return self.lhs
    
    def __neg__(self):
        result = Lazy(self.lhs)
        result.sign = getattr(operator, '__neg__')
        return result

    def __pos__(self):
        result = Lazy(self.lhs)
        result.sign = getattr(operator, '__pos__')
        return result

    def __radd__(self, other):
        return create("__add__", other, self)

    def __rsub__(self, other):
        return create("__sub__", other, self)

    def __rmul__(self, other):
        return create("__mul__", other, self)

    def __rmod__(self, other):
        return create("__mod__", other, self)

    def __rdiv__(self, other):
        return create("__div__", other, self)

    def __rfloordiv__(self, other):
        return create("__floordiv__", other, self)
 
    @wrap
    def __add__(self, other):
        pass 

    @wrap
    def __sub__(self, other):
        pass

    @wrap
    def __div__(self, other):
        pass

    @wrap
    def __floordiv__(self, other):
        pass

    @wrap
    def __mod__(self, other):
        pass

    @wrap
    def __mul__(self, other):
        pass

    def __bool__(self):
        return bool(self.force())

    def __int__(self):
        return int(self.force())
    
    def __float__(self):
        return float(self.force())
   
    def __str__(self):
        return str(self.force())

'''
	st = ""
        if self.op:
            if self.sign:
                st += "("+STR_REPR[self.sign.__name__]+str(self.lhs)+" )"
            st += STR_REPR[self.op.__name__]
        st += str(self.rhs)
        return st
'''

