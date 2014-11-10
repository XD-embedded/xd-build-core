from xd.build.core.data.list import *

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = List(['foo'])
        self.assertEqual(s.get(), ['foo'])

    def test_init_get_2(self):
        s = List([])
        self.assertEqual(s.get(), [])

    def test_init_get_3(self):
        s = List()
        self.assertIsNone(s.get())

    def test_str_1(self):
        s = List(['foo', 'bar'])
        self.assertEqual(str(s), 'List()')

    def test_str_2(self):
        s = List([])
        self.assertEqual(str(s), 'List()')

    def test_str_3(self):
        s = List()
        self.assertEqual(str(s), 'List()')

    def test_set_get(self):
        s = List(['foo'])
        self.assertEqual(s.get(), ['foo'])
        s.set(['bar'])
        self.assertEqual(s.get(), ['bar'])

    def test_append_1(self):
        s = List(['foo'])
        s.append('bar')
        self.assertEqual(s.get(), ['foo', 'bar'])

    def test_append_2(self):
        s = List([])
        s.append('bar')
        self.assertEqual(s.get(), ['bar'])

    def test_append_3(self):
        s = List()
        s.append('bar')
        self.assertEqual(s.get(), ['bar'])

    def test_append_4(self):
        s = List(['foo'])
        s.append('xy')
        s.append('bar')
        self.assertEqual(s.get(), ['foo', 'xy', 'bar'])

    def test_append_typeerror(self):
        s = List(['foo'])
        with self.assertRaises(TypeError):
            s.append(['bar'])

    def test_prepend_1(self):
        s = List(['foo'])
        s.prepend('bar')
        self.assertEqual(s.get(), ['bar', 'foo'])

    def test_prepend_2(self):
        s = List([])
        s.prepend('bar')
        self.assertEqual(s.get(), ['bar'])

    def test_prepend_3(self):
        s = List()
        s.prepend('bar')
        self.assertEqual(s.get(), ['bar'])

    def test_prepend_4(self):
        s = List(['foo'])
        s.prepend('xy')
        s.prepend('bar')
        self.assertEqual(s.get(), ['bar', 'xy', 'foo'])

    def test_prepend_typeerror(self):
        s = List(['foo'])
        with self.assertRaises(TypeError):
            s.prepend(['bar'])

    def test_append_set(self):
        s = List(['foo'])
        s.append('bar')
        s.set(['hello'])
        self.assertEqual(s.get(), ['hello'])

    def test_remove_1(self):
        s = List(['foo', 'bar'])
        s.remove('foo')
        self.assertEqual(s.get(), ['bar'])

    def test_remove_2(self):
        s = List(['foo', 'bar', 'foo'])
        s.remove('foo')
        self.assertEqual(s.get(), ['bar', 'foo'])

    def test_remove_3(self):
        s = List(['foo', 'bar', 'foo'])
        s.remove('foo')
        s.remove('foo')
        self.assertEqual(s.get(), ['bar'])

    def test_remove_4(self):
        s = List(['bar'])
        s.remove('foo')
        self.assertEqual(s.get(), ['bar'])

    def test_extend_1(self):
        s = List(['foo', 'bar'])
        s.extend(['hello', 'world'])
        self.assertEqual(s.get(), ['foo', 'bar', 'hello', 'world'])

    def test_extend_2(self):
        s = List(['foo', 'bar'])
        s.extend([])
        self.assertEqual(s.get(), ['foo', 'bar'])

    def test_sort_1(self):
        s = List(['foo', 'bar', 'hello', 'world'])
        s.sort()
        self.assertEqual(s.get(), ['bar', 'foo', 'hello', 'world'])

    def test_sort_2(self):
        s = List(['foo', 'bar', 'hello', 'world'])
        s.sort(reverse=True)
        self.assertEqual(s.get(), ['world', 'hello', 'foo', 'bar'])

    def test_value_contamination_prepend(self):
        s = List([1])
        self.assertEqual(s.get(), [1])
        s.prepend(2)
        self.assertEqual(s.get(), [2,1])
        self.assertEqual(s.get(), [2,1])
        s.prepend(3)
        self.assertEqual(s.get(), [3,2,1])
        self.assertEqual(s.get(), [3,2,1])

    def test_value_contamination_append(self):
        s = List([1])
        self.assertEqual(s.get(), [1])
        s.append(2)
        self.assertEqual(s.get(), [1,2])
        self.assertEqual(s.get(), [1,2])
        s.append(3)
        self.assertEqual(s.get(), [1,2,3])
        self.assertEqual(s.get(), [1,2,3])

    def test_value_contamination_remove(self):
        s = List([1,2,1,1])
        self.assertEqual(s.get(), [1,2,1,1])
        s.remove(1)
        self.assertEqual(s.get(), [2,1,1])
        self.assertEqual(s.get(), [2,1,1])
        s.remove(1)
        self.assertEqual(s.get(), [2,1])
        self.assertEqual(s.get(), [2,1])

    def test_value_contamination_extend(self):
        s = List([1,2])
        self.assertEqual(s.get(), [1,2])
        s.extend([3,4])
        self.assertEqual(s.get(), [1,2,3,4])
        self.assertEqual(s.get(), [1,2,3,4])

    def test_anonymous_item_append(self):
        from xd.build.core.data.string import String
        s = List([1,2])
        with self.assertRaises(TypeError):
            s.append(String('foo'))

    def test_anonymous_item_prepend(self):
        from xd.build.core.data.string import String
        s = List([1,2])
        with self.assertRaises(TypeError):
            s.prepend(String('foo'))
