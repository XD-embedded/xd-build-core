from xd.build.core.data.dict import *

import unittest

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        s = Dict()
        self.assertIsNone(s.get())

    def test_init_get_2(self):
        s = Dict({})
        self.assertEqual(s.get(), {})

    def test_init_get_3(self):
        s = Dict({'foo': 42, 'bar': 43})
        self.assertEqual(s.get(), {'foo': 42, 'bar': 43})

    def test_str_1(self):
        s = Dict()
        self.assertEqual(str(s), 'Dict()')

    def test_str_2(self):
        s = Dict({})
        self.assertEqual(str(s), 'Dict()')

    def test_str_3(self):
        s = Dict({'foo': 42, 'bar': 43})
        self.assertEqual(str(s), 'Dict()')

    def test_set_get(self):
        s = Dict({'foo': 42})
        self.assertEqual(s.get(), {'foo': 42})
        s.set({'bar': 43})
        self.assertEqual(s.get(), {'bar': 43})

    def test_set_dict(self):
        s = Dict()
        s.set({'bar': 43})
        self.assertEqual(s.get(), {'bar': 43})

    def test_set_none(self):
        s = Dict({'foo': 42})
        self.assertEqual(s.get(), {'foo': 42})
        s.set(None)
        self.assertIsNone(s.get())

    def test_update_1(self):
        s = Dict({'foo': 42})
        s.update({'bar': 43})
        self.assertEqual(s.get(), {'foo': 42, 'bar': 43})

    def test_update_2(self):
        s = Dict({'foo': 42})
        s.update({'bar': 43})
        s.update({'hello': 44})
        self.assertEqual(s.get(), {'foo': 42, 'bar': 43, 'hello': 44})

    def test_update_3(self):
        s = Dict({'foo': 42})
        s.update({'bar': 43})
        s.update({'hello': 44})
        s.update({'bar': 45})
        self.assertEqual(s.get(), {'foo': 42, 'bar': 45, 'hello': 44})

    def test_update_4(self):
        s = Dict({'foo': 42})
        s.update({'bar': 43})
        s.update({'hello': 44})
        s.update({'foo': 45})
        self.assertEqual(s.get(), {'foo': 45, 'bar': 43, 'hello': 44})

    def test_update_5(self):
        s = Dict()
        s.update({'foo': 42})
        self.assertEqual(s.get(), {'foo': 42})

    def test_update_6(self):
        s = Dict({})
        s.update({'foo': 42})
        self.assertEqual(s.get(), {'foo': 42})

    def test_update_str(self):
        s = Dict()
        with self.assertRaises(TypeError):
            s.update('foo')

    def test_update_bool(self):
        s = Dict()
        with self.assertRaises(TypeError):
            s.update(True)

    def test_update_int(self):
        s = Dict()
        with self.assertRaises(TypeError):
            s.update(42)

    def test_update_float(self):
        s = Dict()
        with self.assertRaises(TypeError):
            s.update(3.14)

    def test_update_list(self):
        s = Dict()
        with self.assertRaises(TypeError):
            s.update([1,2])

    def test_update_set(self):
        s = Dict({'foo': 42})
        s.update({'bar': 43})
        s.set({'hello': 'world'})
        self.assertEqual(s.get(), {'hello': 'world'})

    def test_item_1(self):
        s = Dict()
        s['foo'] = 42
        self.assertEqual(s['foo'].get(), 42)

    def test_item_2(self):
        s = Dict()
        s['foo'] = [42]
        self.assertEqual(s['foo'].get(), [42])

    def test_item_3(self):
        s = Dict()
        s['foo'] = [42]
        self.assertEqual(s['foo'].get(), [42])
