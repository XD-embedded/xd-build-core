from xd.build.core.data.namespace import *
from xd.build.core.data.expr import Expression
from xd.build.core.data.string import String

import unittest

class tests(unittest.case.TestCase):

    def setUp(self):
        self.ns = Namespace()

    def test_set_get_1(self):
        self.ns['FOO'] = 'foo'
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_set_get_2(self):
        self.ns['FOO'] = String('foo')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_set2_get_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['FOO'] = 'bar'
        self.assertEqual(self.ns['FOO'].get(), 'bar')

    def test_set_variable(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.ns['BAR'] = self.ns['FOO']
        self.ns['FOO'] = 'hello world'
        self.assertEqual(self.ns['FOO'].get(), 'hello world')
        self.assertEqual(self.ns['BAR'].get(), 'hello world')

    def test_set_bad_type(self):
        self.ns['FOO'] = 'foo'
        with self.assertRaises(TypeError):
            self.ns['FOO'] = 42

    def test_get_keyerror(self):
        with self.assertRaises(KeyError):
            self.ns['FOO']

    def test_del(self):
        self.ns['FOO'] = 'foo'
        del self.ns['FOO']
        with self.assertRaises(KeyError):
            self.ns['FOO']

    def test_eval_source_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.assertEqual(self.ns.eval('FOO+BAR'), 'foobar')

    def test_eval_source_2(self):
        self.ns['FOO'] = 'foo'
        with self.assertRaises(NameError):
            self.ns.eval('FOO+BAR')

    def test_eval_expression_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        expr = Expression('FOO+BAR')
        self.assertEqual(self.ns.eval(expr), 'foobar')

    def test_eval_expression_2(self):
        self.ns['FOO'] = 'foo'
        expr = Expression('FOO+BAR')
        with self.assertRaises(NameError):
            self.ns.eval(expr)

    def test_eval_globals(self):
        self.ns['FOO'] = 'foo'
        BAR = 'bar'
        expr = Expression('FOO+BAR')
        self.assertEqual(self.ns.eval(expr, g={'BAR': BAR}), 'foobar')

    def test_append_variable(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].append(self.ns['BAR'])
        self.assertEqual(self.ns['FOO'].get(), 'foobar')

    def test_append_expr(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].append(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'foobar')

    def test_append_expr_none_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        self.ns['FOO'].append(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_append_expr_none_2(self):
        self.ns['FOO'] = String()
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].append(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'bar')

    #def test_append_expr_typeerror(self):
    #    self.ns['FOO'] = String()
    #    self.ns['BAR'] = 42
    #    self.ns['FOO'].append(Expression('BAR'))
    #    with self.assertRaises(TypeError):
    #        self.ns['FOO'].get()

    def test_prepend_variable(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].prepend(self.ns['BAR'])
        self.assertEqual(self.ns['FOO'].get(), 'barfoo')

    def test_prepend_expr(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].prepend(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'barfoo')

    def test_prepend_expr_none_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        self.ns['FOO'].prepend(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_prepend_expr_none_2(self):
        self.ns['FOO'] = String()
        self.ns['BAR'] = 'bar'
        self.ns['FOO'].prepend(Expression('BAR'))
        self.assertEqual(self.ns['FOO'].get(), 'bar')

    #def test_prepend_expr_typeerror(self):
    #    self.ns['FOO'] = String()
    #    self.ns['BAR'] = 42
    #    self.ns['FOO'].prepend(Expression('BAR'))
    #    with self.assertRaises(TypeError):
    #        self.ns['FOO'].get()

    def test_multibinding(self):
        FOO = self.ns['FOO'] = 'foo'
        with self.assertRaises(MultiBinding):
            self.ns['BAR'] = self.ns['FOO']

    def test_expr_as_init(self):
        FOO = self.ns['FOO'] = 'foo'
        with self.assertRaises(TypeError):
            self.ns['BAR'] = Expression('BAR')

    def test_init_with_unsupported(self):
        with self.assertRaises(TypeError):
            self.ns['BAR'] = set()

    def test_init_with_other_variable(self):
        self.ns['FOO'] = 'foo'
        BAR = String(self.ns['FOO'])
        self.ns['BAR'] = BAR
        self.ns['FOO'] = 'bar'
        self.assertEqual(self.ns['FOO'].get(), 'bar')
        self.assertEqual(self.ns['BAR'].get(), 'bar')
