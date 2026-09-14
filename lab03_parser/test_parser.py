from contextlib import redirect_stdout, redirect_stderr
import io
import unittest
from support import parse_expression
from ast_printer import AstPrinter
from error_handler import ErrorHandler, ParseError


class ParserTests(unittest.TestCase):
    def printed(self, source):
        expression = parse_expression(source)
        self.assertFalse(ErrorHandler.had_error)
        self.assertIsNotNone(expression)
        return AstPrinter().print(expression)

    def test_multiplication_precedence(self):
        self.assertEqual(self.printed('1 + 2 * 3'), '(+ 1.0 (* 2.0 3.0))')

    def test_parentheses(self):
        self.assertEqual(self.printed('(1 + 2) * 3'), '(* (group (+ 1.0 2.0)) 3.0)')

    def test_subtraction_associativity(self):
        self.assertEqual(self.printed('8 - 3 - 1'), '(- (- 8.0 3.0) 1.0)')

    def test_division_associativity(self):
        self.assertEqual(self.printed('16 / 4 / 2'), '(/ (/ 16.0 4.0) 2.0)')

    def test_unary_precedence(self):
        self.assertEqual(self.printed('-1 * 2'), '(* (- 1.0) 2.0)')

    def test_chained_unary(self):
        self.assertEqual(self.printed('!!false'), '(! (! False))')

    def test_comparison_before_equality(self):
        self.assertEqual(self.printed('1 + 2 < 4 == true'), '(== (< (+ 1.0 2.0) 4.0) True)')

    def test_strings(self):
        self.assertEqual(self.printed('"a" + "b"'), '(+ a b)')

    def test_nil(self):
        self.assertEqual(self.printed('nil'), 'nil')

    def assert_parse_error(self, source):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            try:
                parse_expression(source)
            except ParseError:
                pass
        self.assertTrue(ErrorHandler.had_error, 'Invalid expression was silently accepted')

    def test_unmatched_open_parenthesis(self):
        self.assert_parse_error('(1 + 2')

    def test_unexpected_close_parenthesis(self):
        self.assert_parse_error(')')

    def test_missing_operand(self):
        self.assert_parse_error('1 +')

    def test_unexpected_operator(self):
        self.assert_parse_error('* 2')

    def test_empty_group(self):
        self.assert_parse_error('()')


def operator_test(operator):
    def test(self):
        self.assertEqual(self.printed(f'2 {operator} 1'), f'({operator} 2.0 1.0)')
    return test

for name, operator in [('add','+'),('subtract','-'),('multiply','*'),('divide','/'),
                       ('equal','=='),('not_equal','!='),('greater','>'),
                       ('greater_equal','>='),('less','<'),('less_equal','<=')]:
    setattr(ParserTests, 'test_operator_' + name, operator_test(operator))
