"""Practice checks for the Python Lox scanner contract (standard library only)."""
from contextlib import redirect_stdout, redirect_stderr
import io
import unittest

from error_handler import ErrorHandler
from lox_token import Token
from scanner import Scanner
from token_type import TokenType


class ScannerTests(unittest.TestCase):
    def setUp(self):
        ErrorHandler.had_error = False

    def scan(self, source):
        tokens = Scanner(source).scan_tokens()
        self.assertIsInstance(tokens, list)
        self.assertFalse(ErrorHandler.had_error)
        self.assertTrue(tokens, "Scanner must emit EOF even for empty input")
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        self.assertEqual(sum(t.type == TokenType.EOF for t in tokens), 1)
        return tokens

    def names(self, source):
        return [t.type.name for t in self.scan(source)]

    def test_token_fields(self):
        token = Token(TokenType.NUMBER, "12.5", 12.5, 3)
        self.assertEqual((token.type, token.lexeme, token.literal, token.line),
                         (TokenType.NUMBER, "12.5", 12.5, 3))

    def test_token_display_contains_fields(self):
        display = str(Token(TokenType.NUMBER, "001.5", 1.5, 2))
        for value in ("NUMBER", "001.5", "1.5"):
            self.assertIn(value, display)

    def test_empty_input(self):
        token, = self.scan("")
        self.assertEqual((token.lexeme, token.literal, token.line), ("", None, 1))

    def test_single_character_tokens(self):
        self.assertEqual(self.names("(){} ,.-+;/*"), [
            "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
            "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR", "EOF"])

    def test_comparison_operators(self):
        self.assertEqual(self.names("! != = == > >= < <="), [
            "BANG", "BANG_EQUAL", "EQUAL", "EQUAL_EQUAL", "GREATER",
            "GREATER_EQUAL", "LESS", "LESS_EQUAL", "EOF"])

    def test_adjacent_operators(self):
        self.assertEqual(self.names("!=="), ["BANG_EQUAL", "EQUAL", "EOF"])

    def test_all_keywords(self):
        words = "and class else false for fun if nil or print return super this true var while"
        self.assertEqual(self.names(words), [w.upper() for w in words.split()] + ["EOF"])

    def test_identifiers_and_keyword_prefixes(self):
        source = "name _x x2 andy variable True"
        tokens = self.scan(source)
        self.assertEqual([t.type.name for t in tokens], ["IDENTIFIER"] * 6 + ["EOF"])
        self.assertEqual([t.lexeme for t in tokens[:-1]], source.split())

    def test_numbers(self):
        tokens = self.scan("0 123 45.67")
        self.assertEqual([t.type for t in tokens[:-1]], [TokenType.NUMBER] * 3)
        self.assertEqual([t.literal for t in tokens[:-1]], [0, 123, 45.67])
        self.assertEqual([t.lexeme for t in tokens[:-1]], ["0", "123", "45.67"])

    def test_decimal_requires_fraction_digits(self):
        self.assertEqual(self.names("123. .5"), ["NUMBER", "DOT", "DOT", "NUMBER", "EOF"])

    def test_minus_is_separate_token(self):
        self.assertEqual(self.names("-12"), ["MINUS", "NUMBER", "EOF"])

    def test_string_literal_and_lexeme(self):
        token = self.scan('"hello world"')[0]
        self.assertEqual((token.type, token.lexeme, token.literal),
                         (TokenType.STRING, '"hello world"', "hello world"))

    def test_empty_string(self):
        token = self.scan('""')[0]
        self.assertEqual((token.type, token.literal), (TokenType.STRING, ""))

    def test_multiline_string_advances_line(self):
        tokens = self.scan('"first\nsecond"\nvar')
        self.assertEqual(tokens[0].literal, "first\nsecond")
        self.assertEqual(tokens[1].line, 3)

    def test_whitespace_and_lines(self):
        tokens = self.scan(" \t\r\nvar\nname")
        self.assertEqual([t.line for t in tokens], [2, 3, 3])

    def test_comments(self):
        tokens = self.scan("// ignored @ characters\nvar // end")
        self.assertEqual([t.type.name for t in tokens], ["VAR", "EOF"])
        self.assertEqual(tokens[0].line, 2)

    def test_slashes_inside_string(self):
        token = self.scan('"https://example.org"')[0]
        self.assertEqual(token.literal, "https://example.org")

    def test_literal_keyword_values(self):
        tokens = self.scan("true false nil")
        self.assertIs(tokens[0].literal, True)
        self.assertIs(tokens[1].literal, False)
        self.assertIsNone(tokens[2].literal)

    def test_small_program(self):
        tokens = self.scan('var answer = 42; print "ok";')
        self.assertEqual([t.type.name for t in tokens], [
            "VAR", "IDENTIFIER", "EQUAL", "NUMBER", "SEMICOLON",
            "PRINT", "STRING", "SEMICOLON", "EOF"])
        self.assertEqual(tokens[1].lexeme, "answer")
        self.assertEqual(tokens[3].literal, 42)

    def test_fresh_scanner_has_independent_state(self):
        self.scan("var x = 1;")
        self.assertEqual(self.names("print"), ["PRINT", "EOF"])

    def assert_error(self, source, phrase, line):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            Scanner(source).scan_tokens()
        message = stdout.getvalue() + stderr.getvalue()
        self.assertTrue(ErrorHandler.had_error)
        self.assertIn(phrase.lower(), message.lower())
        self.assertIn(f"line {line}", message.lower())

    def test_unexpected_character(self):
        self.assert_error("\n@", "unexpected character", 2)

    def test_unterminated_string(self):
        self.assert_error('"unfinished', "unterminated string", 1)
