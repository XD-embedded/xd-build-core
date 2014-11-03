from xd.build.core.data.namespace import *
from xd.build.core.data.expr import Expression
from xd.build.core.data.string import String
from xd.build.core.data.num import *

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

    def test_set_get_bool(self):
        self.ns['FOO'] = True
        self.assertEqual(self.ns['FOO'].get(), True)

    def test_set_get_int(self):
        self.ns['FOO'] = 42
        self.assertEqual(self.ns['FOO'].get(), 42)

    def test_set_get_float(self):
        self.ns['FOO'] = 3.14
        self.assertEqual(self.ns['FOO'].get(), 3.14)

    def test_set_bad_type(self):
        self.ns['FOO'] = 'foo'
        with self.assertRaises(TypeError):
            self.ns['FOO'] = 42

    def test_get_keyerror(self):
        with self.assertRaises(KeyError):
            self.ns['FOO']

    def test_get_typeerror(self):
        self.ns['FOO'] = String()
        self.ns['I'] = 42
        self.ns['FOO'] = Expression('I')
        with self.assertRaises(TypeError):
            self.ns['FOO'].get()

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

    def test_append_to_expr(self):
        self.ns['FOO'] = 'foo'
        self.ns['FOOBAR'] = String(Expression('FOO'))
        self.ns['FOOBAR'].append('bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foobar')

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

    def test_append_expr_typeerror(self):
        self.ns['FOO'] = String()
        self.ns['BAR'] = 42
        self.ns['FOO'].append(Expression('BAR'))
        with self.assertRaises(TypeError):
            self.ns['FOO'].get()

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

    def test_prepend_expr_typeerror(self):
        self.ns['FOO'] = String()
        self.ns['BAR'] = 42
        self.ns['FOO'].prepend(Expression('BAR'))
        with self.assertRaises(TypeError):
            self.ns['FOO'].get()

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
        FOO = String(self.ns['FOO'])
        self.ns['BAR'] = FOO
        self.ns['FOO'] = 'bar'
        self.assertEqual(self.ns['FOO'].get(), 'bar')
        self.assertEqual(self.ns['BAR'].get(), 'bar')

    def test_str_set_if_1(self):
        self.ns['FOOBAR'] = 'foo'
        self.ns['BAR'] = 'b'
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'bar')

    def test_str_set_if_2(self):
        self.ns['FOOBAR'] = 'foo'
        self.ns['BAR'] = ''
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_3(self):
        self.ns['FOOBAR'] = 'foo'
        self.ns['BAR'] = String()
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_4(self):
        self.ns['FOOBAR'] = 'foo'
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_5(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['FOO'] = 'f'
        self.ns['BAR'] = 'b'
        self.ns['FOOBAR'].set_if(Expression('FOO'), 'foo')
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'bar')

    def test_str_set_if_6(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['FOO'] = 'f'
        self.ns['BAR'] = 'b'
        self.ns['FOOBAR'].set_if(Expression('BAR'), 'bar')
        self.ns['FOOBAR'].set_if(Expression('FOO'), 'foo')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_7(self):
        self.ns['FOOBAR'] = 'foo'
        self.ns['BAR'] = 'b'
        self.ns['FOOBAR'].set_if(self.ns['BAR'], 'bar')
        self.assertEqual(self.ns['FOOBAR'].get(), 'bar')

    def test_str_set_if_8(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'] = 'foo'
        self.ns['FOOBAR'].set_if(Expression('BAR'), Expression('FOO'))
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_9(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['BAR'] = 'bar'
        self.ns['FOO'] = 'foo'
        self.ns['FOOBAR'].set_if(Expression('BAR'), self.ns['FOO'])
        self.assertEqual(self.ns['FOOBAR'].get(), 'foo')

    def test_str_set_if_typeerror_1(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['BAR'] = True
        with self.assertRaises(TypeError):
            self.ns['FOOBAR'].set_if(Expression('BAR'), 42)

    def test_str_set_if_typeerror_2(self):
        self.ns['FOOBAR'] = 'hello world'
        self.ns['BAR'] = True
        self.ns['FOO'] = 42
        self.ns['FOOBAR'].set_if(Expression('BAR'), Expression('FOO'))
        with self.assertRaises(TypeError):
            self.ns['FOOBAR'].get()

    def test_str_append_if_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'b'
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foobar')

    def test_str_append_if_2(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = ''
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_append_if_3(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_append_if_4(self):
        self.ns['FOO'] = 'foo'
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_append_if_5(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'b'
        BAR = self.ns['BAR']
        self.ns['FOO'].append_if(BAR, 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foobar')

    def test_str_append_if_6(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        BAR = self.ns['BAR']
        self.ns['FOO'].append_if(BAR, 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_append_if_7(self):
        self.ns['FOO'] = 'foo'
        self.ns['B'] = 'b'
        self.ns['BAR'] = 'bar'
        BAR = self.ns['BAR']
        self.ns['FOO'].append_if(Expression('B'), BAR)
        self.assertEqual(self.ns['FOO'].get(), 'foobar')

    def test_str_append_if_8(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        BAR = self.ns['BAR']
        self.ns['FOO'].append_if(Expression('B'), BAR)
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_append_if_9(self):
        self.ns['FOO'] = 'foo'
        self.ns['X'] = 'x'
        self.ns['Y'] = ''
        self.ns['Z'] = 'z'
        self.ns['FOO'].append_if(Expression('X'), 'xxx')
        self.ns['FOO'].append_if(Expression('Y'), 'yyy')
        self.ns['FOO'].append_if(Expression('Z'), 'zzz')
        self.assertEqual(self.ns['FOO'].get(), 'fooxxxzzz')

    def test_str_append_if_typeerror_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['b'] = True
        with self.assertRaises(TypeError):
            self.ns['FOO'].append_if(Expression('b'), 42)

    def test_str_append_if_typeerror_2(self):
        self.ns['FOO'] = 'foo'
        self.ns['I'] = 42
        self.ns['FOO'].append_if(Expression('I'), Expression('I'))
        with self.assertRaises(TypeError):
            self.ns['FOO'].get()

    def test_str_prepend_if_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'b'
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'barfoo')

    def test_str_prepend_if_2(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = ''
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_prepend_if_3(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_prepend_if_4(self):
        self.ns['FOO'] = 'foo'
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_prepend_if_5(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'b'
        BAR = self.ns['BAR']
        self.ns['FOO'].prepend_if(BAR, 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'barfoo')

    def test_str_prepend_if_6(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = String()
        BAR = self.ns['BAR']
        self.ns['FOO'].prepend_if(BAR, 'bar')
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_prepend_if_7(self):
        self.ns['FOO'] = 'foo'
        self.ns['B'] = 'b'
        self.ns['BAR'] = 'bar'
        BAR = self.ns['BAR']
        self.ns['FOO'].prepend_if(Expression('B'), BAR)
        self.assertEqual(self.ns['FOO'].get(), 'barfoo')

    def test_str_prepend_if_8(self):
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'
        BAR = self.ns['BAR']
        self.ns['FOO'].prepend_if(Expression('B'), BAR)
        self.assertEqual(self.ns['FOO'].get(), 'foo')

    def test_str_prepend_if_9(self):
        self.ns['FOO'] = 'foo'
        self.ns['X'] = 'x'
        self.ns['Y'] = ''
        self.ns['Z'] = 'z'
        self.ns['FOO'].prepend_if(Expression('X'), 'xxx')
        self.ns['FOO'].prepend_if(Expression('Y'), 'yyy')
        self.ns['FOO'].prepend_if(Expression('Z'), 'zzz')
        self.assertEqual(self.ns['FOO'].get(), 'zzzxxxfoo')

    def test_str_prepend_if_typeerror_1(self):
        self.ns['FOO'] = 'foo'
        self.ns['b'] = True
        with self.assertRaises(TypeError):
            self.ns['FOO'].prepend_if(Expression('b'), 42)

    def test_str_prepend_if_typeerror_2(self):
        self.ns['FOO'] = 'foo'
        self.ns['I'] = 42
        self.ns['FOO'].prepend_if(Expression('I'), Expression('I'))
        with self.assertRaises(TypeError):
            self.ns['FOO'].get()

    def test_str_string(self):
        self.ns['FOO'] = ''
        self.assertEqual(str(self.ns['FOO']), 'String(FOO)')

    def test_str_bool(self):
        self.ns['FOO'] = True
        self.assertEqual(str(self.ns['FOO']), 'Bool(FOO)')

    def test_str_int(self):
        self.ns['FOO'] = 42
        self.assertEqual(str(self.ns['FOO']), 'Int(FOO)')

    def test_str_float(self):
        self.ns['FOO'] = 3.14
        self.assertEqual(str(self.ns['FOO']), 'Float(FOO)')

    def test_list_set_if_1(self):
        self.ns['FOOBAR'] = ['foo']
        self.ns['BAR'] = True
        self.ns['FOOBAR'].set_if(Expression('BAR'), ['bar'])
        self.assertEqual(self.ns['FOOBAR'].get(), ['bar'])

    def test_list_set_if_2(self):
        self.ns['FOOBAR'] = ['foo']
        self.ns['BAR'] = False
        self.ns['FOOBAR'].set_if(Expression('BAR'), ['bar'])
        self.assertEqual(self.ns['FOOBAR'].get(), ['foo'])

    def test_list_set_if_3(self):
        self.ns['FOOBAR'] = ['foo']
        self.ns['FOOBAR'].set_if(Expression('BAR'), ['bar'])
        self.assertEqual(self.ns['FOOBAR'].get(), ['foo'])

    def test_list_prepend_if_1(self):
        self.ns['FOO'] = ['foo']
        self.ns['BAR'] = True
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['bar', 'foo'])

    def test_list_prepend_if_2(self):
        self.ns['FOO'] = ['foo']
        self.ns['BAR'] = False
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['foo'])

    def test_list_prepend_if_3(self):
        self.ns['FOO'] = ['foo']
        self.ns['FOO'].prepend_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['foo'])

    def test_list_append_if_1(self):
        self.ns['FOO'] = ['foo']
        self.ns['BAR'] = True
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['foo', 'bar'])

    def test_list_append_if_2(self):
        self.ns['FOO'] = ['foo']
        self.ns['BAR'] = False
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['foo'])

    def test_list_append_if_3(self):
        self.ns['FOO'] = ['foo']
        self.ns['FOO'].append_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['FOO'].get(), ['foo'])

    def test_list_remove_1(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = 'bar'
        self.ns['L'].remove(Expression('BAR'))
        self.assertEqual(self.ns['L'].get(), ['foo'])

    def test_list_remove_2(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = 'bar'
        self.ns['L'].remove(self.ns['BAR'])
        self.assertEqual(self.ns['L'].get(), ['foo'])

    def test_list_remove_if_1(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = True
        self.ns['L'].remove_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['L'].get(), ['foo'])

    def test_list_remove_if_2(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = False
        self.ns['L'].remove_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['L'].get(), ['foo', 'bar'])

    def test_list_remove_if_3(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['L'].remove_if(Expression('BAR'), 'bar')
        self.assertEqual(self.ns['L'].get(), ['foo', 'bar'])

    def test_list_extend_if_1(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = True
        self.ns['L'].extend_if(Expression('BAR'), ['hello', 'world'])
        self.assertEqual(self.ns['L'].get(), ['foo', 'bar', 'hello', 'world'])

    def test_list_extend_if_2(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['BAR'] = False
        self.ns['L'].extend_if(Expression('BAR'), ['hello', 'world'])
        self.assertEqual(self.ns['L'].get(), ['foo', 'bar'])

    def test_list_extend_if_3(self):
        self.ns['L'] = ['foo', 'bar']
        self.ns['L'].extend_if(Expression('BAR'), ['hello', 'world'])
        self.assertEqual(self.ns['L'].get(), ['foo', 'bar'])

