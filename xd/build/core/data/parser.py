import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


from .namespace import *
from .expr import *
from .string import *
from .num import *
from .list import *
from .dict import *
import ast


__all__ = ['Parser', 'SyntaxError']


class SyntaxError(Exception):
    pass


class Parser(object):

    constructors = ['String', 'Bool', 'Int', 'Float', 'List', 'Dict']

    def __init__(self):
        self.backlog = ast.Module()
        self.backlog.body = []

    def parse(self, path):
        self.expression_store = ExpressionStore('_expr')
        self.namespace = Namespace()
        self.globals = {
            '_expr': self.expression_store.expressions,
            '_namespace': self.namespace
        }
        for constructor in self.constructors:
            self.globals[constructor] = eval(constructor)
        source = open(path).read()
        statements = ast.parse(source, path)
        for statement in statements.body:
            self.parse_statement(statement)
        self.process_backlog(self.globals, self.namespace, path)
        return self.namespace

    def parse_statement(self, statement):
        if isinstance(statement, ast.Assign):
            statement.value = self.parse_value(statement.value)
            self.backlog.body.append(statement)
        elif isinstance(statement, ast.Expr):
            assert isinstance(statement.value, ast.Call)
            statement.value.args = [
                self.parse_value(arg, strwrap=False)
                for arg in statement.value.args]
            for i in range(len(statement.value.keywords)):
                keyword = statement.value.keywords[i]
                keyword.value = self.expression_store.store(keyword.value)
            self.backlog.body.append(statement)
        else:
            raise SyntaxError('unsupported statement: %s'%(
                statement.__class__.__name__))

    def parse_value(self, value, strwrap=True):
        if type(value) in (ast.Str, ast.Num, ast.NameConstant):
            return value
        elif isinstance(value, ast.List):
            value.elts = [self.parse_value(e) for e in value.elts]
            return value
        elif isinstance(value, ast.Dict):
            value.values = [self.parse_value(v) for v in value.values]
            return value
        elif (strwrap and
              isinstance(value, ast.BinOp) and
              isinstance(value.left, ast.Str) and
              isinstance(value.op, ast.Mod)):
            statement = ast.copy_location(ast.Call(
                func=ast.Name(ctx=ast.Load(), id='String'),
                args=[self.expression_store.store(value),
                      ast.Name(ctx=ast.Load(), id='_namespace')],
                keywords=[]), value)
            ast.fix_missing_locations(statement)
            return statement
        elif (strwrap and
              isinstance(value, ast.Call) and
              isinstance(value.func, ast.Attribute) and
              isinstance(value.func.value, ast.Str)):
            statement = ast.copy_location(ast.Call(
                func=ast.Name(ctx=ast.Load(), id='String'),
                args=[self.expression_store.store(value),
                      ast.Name(ctx=ast.Load(), id='_namespace')],
                keywords=[]), value)
            ast.fix_missing_locations(statement)
            return statement
        elif (isinstance(value, ast.Call) and
              hasattr(value.func, 'id') and
              value.func.id in self.constructors):
            value.args = [ self.expression_store.store(arg)
                           for arg in value.args]
            return value
        else:
            return self.expression_store.store(value)

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
        if type(value) in (ast.Str, ast.Num, ast.List, ast.Dict,
                           ast.NameConstant):
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
