from contextlib import redirect_stdout, redirect_stderr
import io
import unittest
from support import parse_program
from environment import Environment
from lox_token import Token
from token_type import TokenType
from error_handler import ErrorHandler


class EnvironmentTests(unittest.TestCase):
    def name(self, name):
        return Token(TokenType.IDENTIFIER, name, None, 1)

    def test_define_get_assign(self):
        env = Environment()
        env.define('a', 1)
        self.assertEqual(env.get(self.name('a')), 1)
        env.assign(self.name('a'), 2)
        self.assertEqual(env.get(self.name('a')), 2)

    def test_enclosing_lookup_and_assignment(self):
        outer = Environment()
        outer.define('a', 1)
        inner = Environment(outer)
        self.assertEqual(inner.get(self.name('a')), 1)
        inner.assign(self.name('a'), 2)
        self.assertEqual(outer.get(self.name('a')), 2)

    def test_shadowing_is_local(self):
        outer = Environment()
        outer.define('a', 1)
        inner = Environment(outer)
        inner.define('a', 2)
        self.assertEqual(inner.get(self.name('a')), 2)
        self.assertEqual(outer.get(self.name('a')), 1)

    def test_panic_mode_recovers_to_later_statements(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            statements = parse_program('var bad = ; print 7; var other = ; print 8;')
        self.assertTrue(ErrorHandler.had_error)
        values = [s.expression.value for s in statements if type(s).__name__ == 'Print']
        self.assertEqual(values, [7, 8], 'Recovery should retain valid statements after each error')
