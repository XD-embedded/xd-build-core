from xd.build.core.data.string import *

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = String('foo')
        self.assertEqual(s.get(), 'foo')

    def test_init_get_2(self):
        s = String('')
        self.assertEqual(s.get(), '')

    def test_init_get_3(self):
        s = String()
        self.assertIsNone(s.get())

    def test_str_1(self):
        s = String('foo')
        self.assertEqual(str(s), 'foo')

    def test_str_2(self):
        s = String('')
        self.assertEqual(str(s), '')

    def test_str_3(self):
        s = String()
        self.assertEqual(str(s), '')

    def test_set_get(self):
        s = String('foo')
        self.assertEqual(s.get(), 'foo')
        s.set('bar')
        self.assertEqual(s.get(), 'bar')

    def test_len_1(self):
        s = String('foobar')
        self.assertEqual(len(s), 6)

    def test_getitem_1(self):
        s = String('foobar')
        self.assertEqual(s[3], 'b')

    def test_getitem_2(self):
        s = String('foobar')
        with self.assertRaises(IndexError):
            s[6]

    def test_contains_1(self):
        s = String('foobar')
        self.assertTrue('f' in s)
        self.assertTrue('o' in s)
        self.assertTrue('b' in s)
        self.assertTrue('a' in s)
        self.assertTrue('r' in s)

    def test_contains_2(self):
        s = String('foobar')
        self.assertFalse('x' in s)
        self.assertFalse('y' in s)
        self.assertFalse('z' in s)

    def test_index_1(self):
        s = String('foobar')
        self.assertEqual(s.index('f'), 0)
        self.assertEqual(s.index('o'), 1)
        self.assertEqual(s.index('b'), 3)
        self.assertEqual(s.index('a'), 4)
        self.assertEqual(s.index('r'), 5)

    def test_index_2(self):
        s = String('foobar')
        with self.assertRaises(ValueError):
            s.index('x')

    def test_index_3(self):
        s = String('foobar')
        self.assertEqual(s.index('o', 2), 2)

    def test_index_4(self):
        s = String('foobar')
        with self.assertRaises(ValueError):
            s.index('o', 3)

    def test_index_5(self):
        s = String('foobar')
        with self.assertRaises(ValueError):
            s.index('b', end=2)

    def test_count_0(self):
        s = String('foobar')
        self.assertEqual(s.count('x'), 0)

    def test_count_1(self):
        s = String('foobar')
        self.assertEqual(s.count('f'), 1)

    def test_count_2(self):
        s = String('foobar')
        self.assertEqual(s.count('o'), 2)

    def test_append_1(self):
        s = String('foo')
        s.append('bar')
        self.assertEqual(s.get(), 'foobar')

    def test_append_2(self):
        s = String('')
        s.append('bar')
        self.assertEqual(s.get(), 'bar')

    def test_append_3(self):
        s = String('foo')
        s.append('')
        self.assertEqual(s.get(), 'foo')

    def test_append_4(self):
        s = String('foo')
        s.append('xy')
        s.append('bar')
        self.assertEqual(s.get(), 'fooxybar')

    def test_append_typeerror(self):
        s = String('foo')
        with self.assertRaises(TypeError):
            s.append(42)

    def test_append_invalid(self):
        s = String('foo')
        s.append('xy')
        s.append('bar')
        self.assertEqual(s.get(), 'fooxybar')

    def test_prepend_1(self):
        s = String('foo')
        s.prepend('bar')
        self.assertEqual(s.get(), 'barfoo')

    def test_prepend_2(self):
        s = String('')
        s.prepend('bar')
        self.assertEqual(s.get(), 'bar')

    def test_prepend_3(self):
        s = String('foo')
        s.prepend('')
        self.assertEqual(s.get(), 'foo')

    def test_prepend_4(self):
        s = String('foo')
        s.prepend('xy')
        s.prepend('bar')
        self.assertEqual(s.get(), 'barxyfoo')

    def test_prepend_typeerror(self):
        s = String('foo')
        with self.assertRaises(TypeError):
            s.prepend(42)

    def test_append_set(self):
        s = String('foo')
        s.append('bar')
        s.set('hello')
        self.assertEqual(s.get(), 'hello')
