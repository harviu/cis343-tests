import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from support import PROJECT
from ast_printer import AstPrinter
from expr import Binary, Grouping, Literal, Unary
from lox_token import Token
from token_type import TokenType


class AstTests(unittest.TestCase):
    def token(self, kind, lexeme):
        return Token(kind, lexeme, None, 1)

    def test_assignment_example(self):
        expression = Binary(Unary(self.token(TokenType.MINUS, '-'), Literal(123)),
                            self.token(TokenType.STAR, '*'), Grouping(Literal(45.67)))
        self.assertEqual(AstPrinter().print(expression), '(* (- 123) (group 45.67))')

    def test_literal(self):
        self.assertEqual(AstPrinter().print(Literal(42)), '42')

    def test_nil_literal(self):
        self.assertEqual(AstPrinter().print(Literal(None)), 'nil')

    def test_string_literal(self):
        self.assertEqual(AstPrinter().print(Literal('hello')), 'hello')

    def test_nested_grouping(self):
        self.assertEqual(AstPrinter().print(Grouping(Grouping(Literal(1)))), '(group (group 1))')

    def test_nested_unary(self):
        expression = Unary(self.token(TokenType.BANG, '!'), Unary(self.token(TokenType.MINUS, '-'), Literal(2)))
        self.assertEqual(AstPrinter().print(expression), '(! (- 2))')

    def test_binary_child_order(self):
        expression = Binary(Literal(8), self.token(TokenType.SLASH, '/'), Literal(2))
        self.assertEqual(AstPrinter().print(expression), '(/ 8 2)')

    def test_independent_printer_calls(self):
        printer = AstPrinter()
        printer.print(Grouping(Literal(1)))
        self.assertEqual(printer.print(Literal(2)), '2')

    def test_generator_creates_usable_expression_classes(self):
        generator = PROJECT / 'tool/generate_ast.py'
        self.assertTrue(generator.is_file(), 'Provide tool/generate_ast.py OUTPUT_DIRECTORY')
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'generated'
            result = subprocess.run([sys.executable, str(generator), str(output)],
                                    cwd=temp, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((output / 'expr.py').is_file())
            spec = importlib.util.spec_from_file_location('generated_expr', output / 'expr.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            left, right, operator = module.Literal(1), module.Literal(2), object()
            binary = module.Binary(left, operator, right)
            self.assertIsInstance(binary, module.Expr)
            self.assertIs(binary.left, left)
            self.assertIs(binary.right, right)
            self.assertIs(binary.operator, operator)
            self.assertIs(module.Grouping(binary).expression, binary)
            unary = module.Unary(operator, right)
            self.assertIs(unary.operator, operator)
            self.assertIs(unary.right, right)
            self.assertEqual(left.value, 1)
