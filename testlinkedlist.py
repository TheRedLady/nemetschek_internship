import unittest
import linkedlist as l

class TestList(unittest.TestCase):

    def testStr(self):
        tst = l.List(1, 2, 3)
        self.assertEqual(str(tst), "<1, 2, 3>")
        tst = l.List()
        self.assertEqual(str(tst), "<>")

    def testCreate(self):
        t =l.List.create(4,5,6)
        g = l.List(1,2,3)
        nil = l.List()
        self.assertEqual(t.list, [4,5,6])
        self.assertEqual(g.list, [1,2,3])
        self.assertEqual(nil.list, [])

    def testIndexing(self):
        tst = l.List(0,1,2,3,4,5,6,7,8,9)
        self.assertEqual(tst[2], 2)
        self.assertEqual(tst[-1], 9)
        self.assertEqual([item for item in tst], [0,1,2,3,4,5,6,7,8,9])


if __name__ == '__main__':
    unittest.main()
