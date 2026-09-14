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

Scanner API checks continue through every stage. File and interactive entry-point
plumbing are checked with a mocked `Lox.run`; the real scanner CLI output is checked
while Lab 1 is the current stage. Once a later lab changes CLI output, only that
historical CLI check is skipped, not the scanner tests.

## Lab 2: AST generator and printer

- `expr.Binary(left, operator, right)`, `Unary(operator, right)`,
  `Grouping(expression)`, and `Literal(value)` preserve those fields.
- `ast_printer.AstPrinter().print(expression)` returns the parenthesized string.
- The assignment example must print `(* (- 123) (group 45.67))`.
- `python tool/generate_ast.py OUTPUT_DIRECTORY` creates usable classes in
  `OUTPUT_DIRECTORY/expr.py`. Generation happens in a temporary directory and
  must not depend on writing over the student's source tree.

## Lab 3: parser

- `Parser(Scanner(source).scan_tokens()).expression()` returns an expression AST.
  This interface remains available when `parse()` changes to parse statements.
- Precedence, left associativity, grouping, all specified operators, and invalid
  expressions are checked. Syntax errors set `ErrorHandler.had_error` and may
  raise `ParseError` from this lower-level API.
- AST printing follows the provided Python example, including `1.0` for scanned
  numbers, `True`/`False` for Python boolean AST literals, and `nil` for None.
- The CLI prints an AST while Lab 3 is the current stage. That historical CLI
  assertion is skipped in later stages while the parser API suite keeps running.

## Lab 4: expression evaluation

- `Interpreter().evaluate(expression)` returns the expression value.
- Invalid operands and division by zero raise `LoxRuntimeError`, rather than an
  uncaught host-language exception. This is the baseline error-reporting policy;
  an approved alternate division-by-zero value needs an adjusted test.
- Baseline `+` accepts two numbers or two strings and rejects a mixed pair.
- Tests check boolean/nil negation, not a specific truthiness policy for 0 or an
  empty string; students must explain those design choices in their reports.
- Calculator CLI output and handled type errors are checked at the Lab 4 stage.
  In later stages the CLI requires statements and expression API tests continue.

## Labs 5–10: complete programs

`python src/lox.py SOURCE_FILE` executes a UTF-8 program. Normal execution exits
with 0; language errors exit with a nonzero code, a relevant diagnostic, and no
Python traceback. Diagnostics are matched by relevant words, not exact wording.
Each program runs in a fresh subprocess with a five-second timeout.

Numeric output accepts `3` or `3.0`; boolean output accepts `true` or `True`;
None prints as `nil`. String lines match exactly. Extra output is a failure.

Each suite's `cases.json` contains named input programs, expected output or error
patterns, and the requirement being checked. A wrong syntax error cannot satisfy
an unrelated runtime error test simply because both exit with a nonzero code.

- **Lab 5:** `Environment(enclosing=None)`, `define(str, value)`, `get(Token)`,
  and `assign(Token, value)` are directly tested. `Parser.parse()` returns a list
  of statements; panic recovery must retain valid statements after malformed
  declarations. AST nodes use `Print.expression` and `Literal.value`.
- **Lab 6:** executable `if`, `while`, and `for`; `for` desugars into `While` and
  block/expression nodes in `stmt`/`expr`. `for (;;)` has a true condition.
- **Lab 7:** callability, arity, parameters, returns and native `clock()`.
  Closures are not required until Lab 8. No wall-clock timestamp is hard-coded.
- **Lab 8:** `Resolver(interpreter).resolve(statements)` records distances by
  calling `interpreter.resolve(expression, depth)`. Closure and binding examples
  from the assignment run through the actual CLI, including the resolver pass.
- **Lab 9:** class construction, fields, methods, `this`, and `init`.
- **Lab 10:** `class Child < Parent`, method inheritance/override, and `super`.

## Design choices and manual grading

These suites target the selected Python Lox reference track, not every permitted
language design. Undefined-variable errors, global redeclaration, rejecting
local redeclaration/self-initialization, nearest-if dangling-else binding, and
rejecting a bare declaration as an if body follow the reference track. Approve
and adapt tests for allowed alternatives before grading those students.

Extra credit (mixed-type coercion, alternate division semantics, break, extra
native functions, static methods, getters, and other approved extensions) is not
required by these baseline tests. In particular, an approved extra-credit change
may require replacing a baseline policy test rather than counting it as wrong.

Reports, screenshots, grammar/semantic explanations, algorithm explanations,
readability, attribution, and the course rubric require manual review. The
checks are not points or a complete grade. See `COVERAGE.md` for the per-lab map.
