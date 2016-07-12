"""
Creation

>>> l = Cons(1, Cons(2, Cons(3, Cons(4, Cons(5, nil)))))
>>> l
<1, 2, 3, 4, 5>
>>> l = List.create(1, 2, 3, 4, 5)
>>> l
<1, 2, 3, 4, 5>

Iteration

>>> [li + 1 for li in l]
[2, 3, 4, 5, 6]

Indexing:

>>> l[1]
2
>>> l[-2]
4

"""


class List:

    def __init__(self,*args):
        self.list = list(args)
        self.isNil = self.list==[]

    @classmethod
    def create(cls, *args):
        return List(*args)

    def __iter__(self):
        for item in self.list:
            yield item

    def __getitem__(self, index):
        return self.list[index]

    def __repr__(self):
        return "<" + str(self.list)[1:-1] + ">"



def Cons(fst, snd):
    args = [fst]
    if hasattr(snd, 'isNil'):
        args.extend(snd.list)
    else:
        args.append(snd)
    return List.create(*args)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
