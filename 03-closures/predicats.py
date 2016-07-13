

def safe_call(function, arg):
    def cll(narg):
        if function.__code__.co_argcount > 1: 
            return function(narg, arg) 
        return function(narg)
    return cll
        
       
class Pred(object):
    
    def __init__(self, f, arg=None):
        self.arg_count = f.__code__.co_argcount
        self.arg = arg 
        self.func = f 

    def __call__(self, *args):
        if self.arg != None:
            return safe_call(self.func, self.arg)(args[0])
        if args:
            if self.arg_count == 1:
                return safe_call(self.func, self.arg)(args[0])
            return Pred(self.func, arg=args[0])
        return Pred(self.func, arg=True)
            
    def __and__(self, other):
        f = composite(self.func, self.arg, other.func, other.arg)
        return Pred(lambda arg: all(f(arg)), arg=True)

    def __or__(self, other):
        f = composite(self.func, self.arg, other.func, other.arg)
        return Pred(lambda arg: any(f(arg)), arg=True) 

    def __rshift__(self, other):
        f = composite(self.func, self.arg, other.func, other.arg)
        g = lambda arg: f(arg)[1] if f(arg)[0] else True
        return Pred(g, arg=True) 

    def __invert__(self): 
        return Pred(lambda arg1, arg2: not self.func(arg1,arg2), arg=self.arg)

def composite(f, farg, g, garg):
    def new_func(arg):
        result = []
        result.append(safe_call(f,farg)(arg))
        result.append(safe_call(g,garg)(arg))
        return result
    return new_func 
        
        
gt = Pred(lambda x, y: x > y)
eq = Pred(lambda x, y: x == y)
lt = Pred(lambda x, y: x < y)
oftype = Pred(lambda t, arg: isinstance(t, arg))
present = Pred(lambda el: el != None)
            

def pred(f):
    return Pred(f)

def for_any(*predicates):
    def check_pr(arg):
        for pred in predicates:
            if pred(arg):
                return True
        return False
    return pred(check_pr)


def for_all(*predicates):
    def check_pr(arg):
        for pred in predicates:
            if not pred(arg):
                return False
        return True
    return pred(check_pr)
