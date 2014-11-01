import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .namespace import *
from .expr import *
from .string import *
import ast


__all__ = ['Parser', 'SyntaxError']


class SyntaxError(Exception):
    pass


class Parser(object):

    def __init__(self):
        self.backlog = ast.Module()
        self.backlog.body = []

    def parse(self, path):
        expression_store = ExpressionStore('_expr')
        g = {'_expr': expression_store.expressions,
             'String': String}
        l = Namespace()
        source = open(path).read()
        statements = ast.parse(source, path)
        for statement in statements.body:
            if isinstance(statement, ast.Assign):
                if type(statement.value) in (ast.Str,):
                    self.backlog.body.append(statement)
                elif (isinstance(statement.value, ast.Call) and
                      hasattr(statement.value.func, 'id') and
                      statement.value.func.id in ('String',)):
                    statement.value.args = [
                        expression_store.store(arg)
                        for arg in statement.value.args]
                    self.backlog.body.append(statement)
                else:
                    statement.value = expression_store.store(statement.value)
                    self.backlog.body.append(statement)
            elif isinstance(statement, ast.Expr):
                self.backlog.body.append(statement)
            else:
                raise SyntaxError('unsupported statement: %s'%(
                    statement.__class__.__name__))
        self.process_backlog(g, l, path)
        return l

    def process_backlog(self, g, l, path):
        if not self.backlog.body:
            return
        code = compile(self.backlog, path, 'exec')
        exec(code, g, l)


class ExpressionStore(object):

    def __init__(self, id):
        self.expressions = []
        self.id = id

    def store(self, value):
        if type(value) in (ast.Str,):
            return value
        expr = Expression(value)
        self.expressions.append(expr)
        ref = ast.Subscript()
        ref.ctx = ast.Load()
        ref.slice = ast.Index()
        ref.slice.value = ast.Num()
        ref.slice.value.n = len(self.expressions) - 1
        ref.value = ast.Name()
        ref.value.ctx = ast.Load()
        ref.value.id = self.id
        ast.fix_missing_locations(ref)
        return ref
