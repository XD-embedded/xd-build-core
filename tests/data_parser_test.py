from xd.build.core.data.parser import *

from case import *

class tests(ManifestTestCase):

    def setUp(self):
        self.parser = Parser()
        super(tests, self).setUp()

    def test_parse_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('FOO="foo"\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(len(d), 1)

    def test_parse_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('FOO=String("foo")\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(len(d), 1)

    def test_parse_expr_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR="bar"
FOOBAR=String(FOO+BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['FOOBAR'].get(), 'foobar')

    def test_parse_expr_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR="bar"
FOOBAR=String()
FOOBAR=FOO+BAR''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['FOOBAR'].get(), 'foobar')

    def test_parse_append_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
FOOBAR=String(FOO)
FOOBAR.append('bar')
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['FOOBAR'].get(), 'foobar')

    def test_parse_append_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR=String()
FOOBAR=String(FOO)
FOOBAR.append(BAR)
BAR="bar"
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['FOOBAR'].get(), 'foobar')

    def test_parse_str_method(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=String()
FOO="foo".capitalize()
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), 'Foo')

    def test_parse_augassign(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO='foo'
FOO+='bar'
''')
        with self.assertRaises(SyntaxError):
            self.parser.parse('recipe.xd')

    def test_parse_empty_recipe(self):
        with open('recipe.xd', 'w') as f:
            f.write('\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 0)

    def test_parse_comment(self):
        with open('recipe.xd', 'w') as f:
            f.write('# this is a comment line\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 0)
