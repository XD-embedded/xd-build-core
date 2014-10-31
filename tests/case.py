import unittest
import sys
import os
import tempfile
import shutil
import configparser


class XdEmbeddedManifest(object):

    def __init__(self, topdir, layers):
        self.topdir = topdir
        self.configfile = os.path.join(topdir, '.xd')
        self.layers = layers

class XdEmbeddedLayer(object):

    def __init__(self, path, priority):
        self.submodule = os.path.basename(path)
        self.path = path
        self.commit = 'HEAD'
        self.configfile = os.path.join(path, '.xd')
        self._priority = priority

    def priority(self):
        return self._priority

class ManifestTestCase(unittest.case.TestCase):

    def setUp(self):
        self.restore = {}
        self.restore['cwd'] = os.getcwd()
        self.testdir = tempfile.mkdtemp(prefix='unittest-')
        self.layerdir = os.path.join(self.testdir, 'layer')
        os.mkdir(self.layerdir)
        os.chdir(self.layerdir)
        config = configparser.ConfigParser()
        config.add_section('build')
        config['build']['recipes'] = 'recipes/*.xd'
        with open('.xd', 'w') as configfile:
            config.write(configfile)
        self.manifest = XdEmbeddedManifest(
            self.testdir, [XdEmbeddedLayer(self.layerdir, 0)])
        os.mkdir('recipes')
        with open(os.path.join('recipes', 'foo_1.0.xd'), 'w') as f:
            f.write('FOO = "bar"\n')
        with open(os.path.join('recipes', 'bar.xd'), 'w') as f:
            f.write('FOO = "bar"\n')
        os.chdir(self.testdir)

    def tearDown(self):
        os.chdir(self.restore['cwd'])
        shutil.rmtree(self.testdir, ignore_errors=True)

class TestCase(unittest.case.TestCase):

    def setUp(self):
        self.restore = {}
        self.restore['cwd'] = os.getcwd()
        self.testdir = tempfile.mkdtemp(prefix='unittest-')
        os.chdir(self.testdir)

    def tearDown(self):
        os.chdir(self.restore['cwd'])
        shutil.rmtree(self.testdir, ignore_errors=True)
