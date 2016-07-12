class Nat(object):

    def __init__(self, v):
        if isinstance(v, int) and v >= 0:
            self.value = v
        else:
            raise TypeError("Not a natural number")

    @classmethod
    def from_int(cls, number):
        return Nat(number) 

    def __str__(self):
        return str(self.value)

    def is_zero(self):
        return self.value == 0

    def predecessor(self):
        if self.value:
            return Nat(self.value - 1)
        raise NotImplemented("First natural number is zero!")

    def successor(self):
        return Nat(self.value + 1)

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value 
   
    def __mul__(self, other):
        return self.value * other.value

    def __div__(self, other):
        return self.value / other.value

    # add +, -, *, /


class Zero(Nat):

    def __init__(self):
        object.__setattr__(self, "value", 0)

    def __setattr__(self, *args):
        raise TypeError("Object is immutable")
   

class Succ(Nat):

    def __init__(self, nat):
        self.value = nat.value + 1
    

# zero = Zero()

# one = Succ(zero)
