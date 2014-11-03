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
        self.assertEqual(str(s), 'String()')

    def test_str_2(self):
        s = String('')
        self.assertEqual(str(s), 'String()')

    def test_str_3(self):
        s = String()
        self.assertEqual(str(s), 'String()')

    def test_set_get(self):
        s = String('foo')
        self.assertEqual(s.get(), 'foo')
        s.set('bar')
        self.assertEqual(s.get(), 'bar')

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
