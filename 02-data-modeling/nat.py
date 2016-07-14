class Nat(object):

    @classmethod
    def from_int(cls, number):
        n = Zero()
        for i in range(number):
            n = n.successor()
        return n

    def successor(self):
        return Succ(self)

    def __add__(self, other):
        return  self.predecessor() +  other.successor()

    def __sub__(self, other):
        return self.predecessor() + other.predecessor()

    def __mul__(self, other):
         return self + other.predecessor * self

    def __div__(self, other):
        if isinstance(other, Zero):
            raise ZeroDivisionError
        return Nat.from_int(1) + (self - other) / other


class Zero(Nat):
    is_zero = True

    def is_zero(self):
        return is_zero

    def predecessor(self):
        raise Exception

    def to_int(self):
        return 0

    def __add__(self, other):
        return other

    def __mul__(self, other):
        return self

    def __div__(self, other):
        return self

class Succ(Nat):
    is_zero = False

    def is_zero(self):
        return is_zero

    def __init__(self, predecessor):
        self._predecessor = predecessor

    def predecessor(self):
        return self._predecessor

    def to_int(self):
        return 1 + self.predecessor().to_int()


zero = Zero()

one = zero.successor()
