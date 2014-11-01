from xd.build.core.data.expr import *
from xd.build.core.data.namespace import Namespace

import unittest
import ast

class tests(unittest.case.TestCase):

    def setUp(self):
        self.ns = Namespace()
        self.ns['FOO'] = 'foo'
        self.ns['BAR'] = 'bar'

    def test_str_1(self):
        self.ns['FOOBAR'] = ''
        self.ns['FOOBAR'] = Expression('FOO+BAR')
        self.assertEqual(self.ns['FOOBAR'].get(), 'foobar')

    def test_ast_1(self):
        self.ns['FOOBAR'] = ''
        expr = ast.parse('FOO+BAR').body[0].value
        self.ns['FOOBAR'] = Expression(expr)
        self.assertEqual(self.ns['FOOBAR'].get(), 'foobar')

    def test_ast_2(self):
        self.ns['FOOBAR'] = ''
        expr = ast.Expression()
        expr.body = ast.parse('FOO+BAR').body[0].value
        ast.copy_location(expr, expr.body)
        self.ns['FOOBAR'] = Expression(expr)
        self.assertEqual(self.ns['FOOBAR'].get(), 'foobar')

    def test_typeerror(self):
        with self.assertRaises(TypeError):
            Expression(42)
