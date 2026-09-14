# Python Lox practice-test contract

These tests match the reference Python interfaces used in the CIS343 example.
They are not a language-independent grading rubric. Students using another
language or an approved grammar variation need an agreed adapter or test suite.
The original assignment and instructor guidance determine the final grade.

## Lab 1: scanner

- Python 3.12; source modules under `src/`.
- `token_type.TokenType`: enum names in the student template.
- `lox_token.Token(type, lexeme, literal, line)`: public attributes with those names.
- `str(token)` includes token type name, lexeme, and literal representation;
  punctuation separating fields is unrestricted.
- `scanner.Scanner(source).scan_tokens()` returns a list of tokens and exactly
  one final EOF (`lexeme=""`, `literal=None`). Lines begin at 1.
- Numbers support integers and decimal fractions; minus is a separate token.
- Strings are double quoted and may span lines, as in the reference scanner.
- ASCII identifiers begin with a letter or underscore and continue with letters,
  digits, or underscores. Tests do not prescribe Unicode behavior.
- Ignore whitespace and `//` comments. Keywords are case sensitive.
- This course reference stores `True`, `False`, and `None` as the literal values
  of `true`, `false`, and `nil` respectively.
- Report lexical errors with `ErrorHandler.error(line, message)` and set
  `ErrorHandler.had_error`. Messages include the line and either
  `Unexpected character` or `Unterminated string` (case insensitive).

The tests call the scanner API rather than asserting the CLI's token output.
That lets scanner checks keep running when later labs change the CLI to print
ASTs or execute programs. File mode, interactive mode, report quality, grammar
design, and extensions are reviewed separately; these 22 checks are practice
coverage, not a complete automatic grade.

## Later labs

Lab 2 is AST generation/printing and Lab 3 is parsing in the current course
instructions. No tests or interfaces for those labs are released yet. Define the
interface in this document before adding each new suite. Keep earlier APIs
compatible or deliberately update the tests to reflect approved changes.
