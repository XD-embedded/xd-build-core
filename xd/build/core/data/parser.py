import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .namespace import *
import ast


__all__ = ['Parser']


class Parser(object):

    def __init__(self):
        self.backlog = ast.Module()
        self.backlog.body = []
        pass

    def parse(self, path):
        g = {}
        l = Namespace()
        source = open(path).read()
        statements = ast.parse(source, path)
        for statement in statements.body:
            if isinstance(statement, ast.Assign):
                self.backlog.body.append(statement)
            else:
                log.error('unsupported statement: %s',
                          statement.__class__.__name__)
        self.process_backlog(g, l, path)
        return l

    def process_backlog(self, g, l, path):
        if not self.backlog.body:
            return
        code = compile(self.backlog, path, 'exec')
        exec(code, g, l)
