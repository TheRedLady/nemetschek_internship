import unittest
from mock import Mock


import model
import field


class Question(model.Model):

    count = field.IntField(default=0)


class Student(model.Model):

    name = field.CharField(min_length=5)
    faculty_number = field.IntField(null=False)


class TestModel(unittest.TestCase):

    def test_char_field(self):
        class Answer(model.Model):

            text = field.CharField(max_length=10)

        a = Answer()
        a.text = 'a'
        with self.assertRaises(field.ValidationError):
            a.text = 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'
        with self.assertRaises(field.ValidationError):
            a.text = 5

    def test_bool_field(self):
        class Statement(model.Model):

            is_true = field.BooleanField()

        s = Statement(is_true=False)
        s.is_true = True
        with self.assertRaises(field.ValidationError):
            s.is_true = 1
        with self.assertRaises(field.ValidationError):
            s.is_true = 5
        self.assertTrue(s.is_true)
        s.is_true = False
        self.assertFalse(s.is_true)

    def test_student(self):
        bobby = Student(name='Bobby', faculty_number=71562)
        with self.assertRaises(field.ValidationError):
            bobby.name = 'Tony'
        with self.assertRaises(field.ValidationError):
            bobby.name = 50
        with self.assertRaises(field.ValidationError):
            bobby.name = True
        with self.assertRaises(field.ValidationError):
            bobby.name = True
        with self.assertRaises(field.ValidationError):
            bobby.faculty_number = None

    def test_question(self):
        q = Question()
        self.assertEqual(q.count, 0)
        q.count = 1
        with self.assertRaises(field.ValidationError):
            q.count = 'z'

        q = Question(count=3, id=2)
        with self.assertRaises(field.ValidationError):
            q.id = None


if __name__ == '__main__':
    unittest.main()
