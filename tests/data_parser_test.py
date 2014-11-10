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

    def test_parse_set_if_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
FOOBAR=String(FOO)
FOOBAR.set_if(BAR, BAR)
BAR="bar"
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['FOOBAR'].get(), 'bar')

    def test_parse_set_if_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="f"
BAR="b"
FOOBAR=String('hello world')
FOOBAR.set_if(BAR, 'bar')
FOOBAR.set_if(FOO, 'foo')
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'f')
        self.assertEqual(d['BAR'].get(), 'b')
        self.assertEqual(d['FOOBAR'].get(), 'foo')

    def test_parse_set_if_3(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="f"
BAR="b"
FOOBAR=String('hello world')
FOOBAR.set_if(FOO, 'foo')
FOOBAR.set_if(BAR, 'bar')
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'f')
        self.assertEqual(d['BAR'].get(), 'b')
        self.assertEqual(d['FOOBAR'].get(), 'bar')

    def test_parse_set_if_4(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="f"
FOOBAR=String('hello world')
FOOBAR.set_if(FOO=='f', 'foo')
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), 'f')
        self.assertEqual(d['FOOBAR'].get(), 'foo')

    def test_parse_set_if_5(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="f"
FOOBAR=String('hello world')
FOOBAR.set_if(FOO=='f', 'foo')
FOO="g"
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), 'g')
        self.assertEqual(d['FOOBAR'].get(), 'hello world')

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

    def test_parse_append_if_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO='foo'
BAR='bar'
FOO.append_if(BAR, 'baaaar')
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), 'foobaaaar')
        self.assertEqual(d['BAR'].get(), 'bar')

    def test_parse_append_if_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR='bar'
B='b'
FOO.append_if(B, BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foobar')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['B'].get(), 'b')

    def test_parse_append_if_3(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR='bar'
B=''
FOO.append_if(B, BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['B'].get(), '')

    def test_parse_append_if_4(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO="foo"
BAR='bar'
FOO.append_if(B, BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')

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

    def test_parse_bool(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=True
BAR=False
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), True)
        self.assertEqual(d['BAR'].get(), False)

    def test_parse_int_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('FOO=42\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), 42)

    def test_parse_int_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=42
BAR=43
FOOBAR=Int(FOO+BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 42)
        self.assertEqual(d['BAR'].get(), 43)
        self.assertEqual(d['FOOBAR'].get(), 85)

    def test_parse_float_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('FOO=3.14\n')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), 3.14)

    def test_parse_float_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=3.14
BAR=22.7
FOOBAR=Float(FOO+BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 3.14)
        self.assertEqual(d['BAR'].get(), 22.7)
        self.assertEqual(d['FOOBAR'].get(), 25.84)

    def test_str_mod(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO='foo'
BAR='bar'
FOOBAR="%s and %s"%(FOO, BAR)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), 'foo')
        self.assertEqual(d['BAR'].get(), 'bar')
        self.assertEqual(d['FOOBAR'].get(), 'foo and bar')

    def test_list_1(self):
        with open('recipe.xd', 'w') as f:
            f.write("FOO=['foo']\n")
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), ['foo'])

    def test_list_add(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=['foo']
BAR=['bar']
FOOBAR=[]
FOOBAR=FOO+BAR
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 3)
        self.assertEqual(d['FOO'].get(), ['foo'])
        self.assertEqual(d['BAR'].get(), ['bar'])
        self.assertEqual(d['FOOBAR'].get(), ['foo', 'bar'])

    def test_list_sort_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=['foo', 'bar', 'hello', 'world']
FOO.sort()
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), ['bar', 'foo', 'hello', 'world'])

    def test_list_sort_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=['foo', 'bar', 'hello', 'world']
FOO.sort(reverse=True)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), ['world', 'hello', 'foo', 'bar'])

    def test_list_sort_3(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=['foo', 'bar', 'hello', 'world']
FOO.sort(reverse=False)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), ['bar', 'foo', 'hello', 'world'])

    def test_list_strmod_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=List()
libdir = '/usr/lib'
FOO = ['%s/foo.so'%(libdir), H+W, ' '.join([H, W]), H + ' and ' + W]
H = 'hello'
W = 'world'
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 4)
        self.assertEqual(d['libdir'].get(), '/usr/lib')
        self.assertEqual(d['FOO'].get(), ['/usr/lib/foo.so', 'helloworld',
                                          'hello world', 'hello and world'])
        self.assertEqual(d['H'].get(), 'hello')
        self.assertEqual(d['W'].get(), 'world')

    def test_list_strformat_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=List()
libdir = '/usr/lib'
FOO = ['{0}/foo.so'.format(libdir)]
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['libdir'].get(), '/usr/lib')
        self.assertEqual(d['FOO'].get(), ['/usr/lib/foo.so'])

    def test_strformat_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''prefix = '/usr'
libdir = '{0}/lib'.format(prefix)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['prefix'].get(), '/usr')
        self.assertEqual(d['libdir'].get(), '/usr/lib')

    def test_dict_1(self):
        with open('recipe.xd', 'w') as f:
            f.write("FOO={'foo': 42}\n")
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'foo': 42})

    def test_dict_update_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO={'foo': 42}
FOO.update({'bar': 43})
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'foo': 42, 'bar': 43})

    def test_dict_update_if_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO={'foo': 42}
FOO.update_if(BAR, {'bar': 43})
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'foo': 42})

    def test_dict_update_if_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO={'foo': 42}
FOO.update_if(BAR, {'bar': 43})
BAR=True
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), {'foo': 42, 'bar': 43})
        self.assertEqual(d['BAR'].get(), True)

    def test_dict_setitem_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO={}
FOO['bar'] = 43
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'bar': 43})

    def test_dict_setitem_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO=Dict()
FOO['bar'] = 43
''')
        self.parser = Parser()
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'bar': 43})

    def test_dict_setitem_3(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FOO={'foo': 42}
FOO['bar'] = 43
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['FOO'].get(), {'foo': 42, 'bar': 43})

    def test_dict_setitem_4(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = FOO
''')
        d = self.parser.parse('recipe.xd')
        self.assertRaises(NameError, d['D']['foo'].get)

    def test_dict_setitem_5(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = FOO
FOO = 'bar'
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(d['D'].get()['foo'], 'bar')

    def test_dict_getitem_keyerror_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = 42
''')
        d = self.parser.parse('recipe.xd')
        with self.assertRaises(KeyError):
            d['D']['bar']

    def test_dict_getitem_keyerror_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('D=Dict()\n')
        d = self.parser.parse('recipe.xd')
        with self.assertRaises(KeyError):
            d['D']['bar']

    def test_dict_list_1(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = [1, 2]
D['foo'].append(3)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['D'].get(), {'foo': [1, 2, 3]})

    def test_dict_list_2(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = [1, 2]
D['foo'].append_if(FOO, 3)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 1)
        self.assertEqual(d['D'].get(), {'foo': [1, 2]})

    def test_dict_list_3(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
D['foo'] = [1, 2]
D['foo'].append_if(FOO, 3)
FOO=True
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), True)
        self.assertEqual(d['D'].get(), {'foo': [1, 2, 3]})

    def test_dict_list_4(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
FOO = [1,2]
D['foo'] = List(FOO)
FOO.append(3)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), [1, 2, 3])
        self.assertEqual(d['D'].get(), {'foo': [1, 2, 3]})

    def test_dict_list_5(self):
        with open('recipe.xd', 'w') as f:
            f.write('''D={}
FOO = [1,2]
D['foo'] = []
D['foo'] = FOO
FOO.append(3)
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['FOO'].get(), [1, 2, 3])
        self.assertEqual(d['D'].get(), {'foo': [1, 2, 3]})

    def test_dict_list_6(self):
        with open('recipe.xd', 'w') as f:
            f.write('''FILES={}
libdir = '/usr/lib'
FILES['foo'] = ['%s/foo.so'%(libdir)]
FILES['foo'].append('%s/bar.so'%(libdir))
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['libdir'].get(), '/usr/lib')
        self.assertEqual(d['FILES'].get(), {'foo': ['/usr/lib/foo.so',
                                                    '/usr/lib/bar.so']})

    def test_dict_strmod_key(self):
        with open('recipe.xd', 'w') as f:
            f.write('''PKG={}
RECIPE_NAME='foo'
PKG['%s-dev'%(RECIPE_NAME,)] = ['/foobar']
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['RECIPE_NAME'].get(), 'foo')
        self.assertEqual(d['PKG'].get(), {'foo-dev': ['/foobar']})

    def test_dict_strformat_key(self):
        with open('recipe.xd', 'w') as f:
            f.write('''PKG={}
RECIPE_NAME='foo'
PKG['{0}-dev'.format(RECIPE_NAME)] = ['/foobar']
''')
        d = self.parser.parse('recipe.xd')
        self.assertEqual(len(d), 2)
        self.assertEqual(d['RECIPE_NAME'].get(), 'foo')
        self.assertEqual(d['PKG'].get(), {'foo-dev': ['/foobar']})

