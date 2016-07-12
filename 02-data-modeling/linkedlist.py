
class Node(object):

    def __init__(self, value, nxt):
        self.value = value
        self.next = nxt


def Cons(val, nxt):
    if nxt == nil:
        return List(Node(val, nil))
    return List(Node(val, nxt.head))

nil = Node(0, None)


class List(object):

    def __init__(self, start):
        self.head = start

    @classmethod
    def create(cls, *args):
        list_obj = List(nil)
        for item in args[::-1]:
            prev = list_obj.head
            list_obj.head = Node(item, prev)
        return list_obj

    def get_list(self):
        lst = []
        current = self.head
        while current != nil:
            lst.append(current.value)
            current = current.next
        return lst

    def __iter__(self):
        current = self.head
        while current != nil:
            yield current.value
            current = current.next

    def __getitem__(self, index):
        return self.get_list()[index]

    def __repr__(self):
        lst = self.get_list()
        return "<" + str(lst)[1:-1] + ">"


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
