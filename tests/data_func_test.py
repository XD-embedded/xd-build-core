from xd.build.core.data.func import Function

import unittest

def foo():
    return 'foobar'

class tests(unittest.case.TestCase):

    def test_init_get_1(self):
        f = Function()
        self.assertIsNone(f.get())

    def test_init_get_2(self):
        f = Function(None)
        self.assertIsNone(f.get())

    def test_init_get_3(self):
        def foo():
            return 'foobar'
        f = Function(foo)
        self.assertEqual(f.get()(), 'foobar')

    def test_set_get(self):
        def foo():
            return 'foobar'
        def bar():
            return 'barfoo'
        f = Function(foo)
        self.assertEqual(f.get()(), 'foobar')
        f.set(bar)
        self.assertEqual(f.get()(), 'barfoo')

    def test_get_source_1(self):
        f = Function(foo)
        self.assertEqual(f.get_source(), '''
def foo():
    return 'foobar'
''')

    def test_get_source_2(self):
        f = Function()
        self.assertEqual(f.get_source(), None)
