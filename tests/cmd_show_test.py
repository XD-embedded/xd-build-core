from xd.build.core.cmd.show import *

from case import *
import argparse

class ArgsStub(object):
    def __init__(self, recipe):
        self.recipe = recipe

class tests(ManifestTestCase):

    def test_arguments_1(self):
        parser = argparse.ArgumentParser()
        add_arguments(parser)
        args = parser.parse_args(['foobar'])
        self.assertEqual(len(vars(args)), 1)
        self.assertEqual(args.recipe, 'foobar')

    def test_run_foo(self):
        args = ArgsStub('foo')
        run(args, self.manifest, os.environ)
        self.assertRegex(sys.stdout.getvalue(),
                         os.path.join(self.layerdir, 'recipes', 'foo_1.0.xd'))
        self.assertRegex(sys.stdout.getvalue(), "FOO='foo'")

    def test_run_bar(self):
        args = ArgsStub('bar')
        run(args, self.manifest, os.environ)
        self.assertRegex(sys.stdout.getvalue(),
                         os.path.join(self.layerdir, 'recipes', 'bar.xd'))
        self.assertRegex(sys.stdout.getvalue(), "BAR='bar'")

    def test_run_foobar(self):
        args = ArgsStub('foobar')
        with self.assertLogs('xd.build.core.cmd.show', level='ERROR') as log:
            run(args, self.manifest, os.environ)
        self.assertRegex(log.output[0], 'recipe not found')
