class Nat(object):

    @classmethod
    def from_int(cls, number):
        pass

    def is_zero(self):
        pass

    def predecessor(self):
        pass

    def successor(self):
        pass

    # add +, -, *, /


class Zero(Nat):
    pass


class Succ(Nat):

    def __init__(self, nat):
        pass
