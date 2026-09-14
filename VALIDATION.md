# Reference validation

Validated locally on 2026-09-14 with Python 3.13.13 (macOS). The GitHub workflow targets Python 3.12; these new changes have not been run on GitHub.

## Each lab against its corresponding branch

| Suite | Branch commit | Result |
|---|---|---|
| `lab01_scanner` | `scanner` / `c865b79ddd004e2e7fc4cb10b8ea9f055e67dad8` | 25/25 pass |
| `lab02_ast` | `ast_printer` / `611ed69d54b2530a54220acfb57dd3c58d0c8bd0` | 9/9 pass |
| `lab03_parser` | `parser` / `601bc49ac80db9e9dd34ce2801ef1d1433731c13` | 25/25 pass |
| `lab04_interpreter` | `evaluater` / `b1ec9493575a0f1447a2d5646a0ab8fef4614598` | 30/31 pass |
| `lab05_variables` | `statement` / `beba00cd7a1450656bed7e60155aa11f2333c0a3` | 14/18 pass |
| `lab06_control_flow` | `control_flow` / `29c590e770c999561ecd7007610616e2d33e4d29` | 19/19 pass |
| `lab07_functions` | `function_no_closure` / `6b1ae466f8bc4de51637310fb02338a6200411e6` | 14/14 pass |
| `lab08_resolver` | `resolver` / `613af5d8edeca616a3ed4f1a394bc85c34cc49e1` | 13/13 pass |
| `lab09_classes` | `class` / `e4861997506c166f931fbf59a87faadaf0fd027f` | 13/13 pass |
| `lab10_inheritance` | `inheritance` / `4cef07f1b2d6c54946ffee33d6817b4996414152` | 12/12 pass |

**174 of 179 checks pass against the unmodified corresponding branches.** The five failures correspond to two underlying defects. Cumulative validation finds one additional historical scanner regression.

## Findings

1. **Division by zero:** `evaluater:src/interpreter.py:50` executes `left / right` directly. Input `1 / 0` raises Python `ZeroDivisionError` instead of the baseline `LoxRuntimeError`. The same failure persists through the `inheritance` branch. Lab 4 explicitly requires robust runtime handling; an approved special-value alternative needs its own expectation.

2. **Expression statements in Lab 5:** `statement:src/parser.py:40` returns `self.expression()` rather than using `expression_statement()`. It leaves the semicolon unconsumed, so `1 + 2;` and `a = 9;` produce a syntax error. Four program tests fail: assignment, assignment to an enclosing/nearest variable, and discarded expression results. This is fixed in the later `control_flow` branch.

3. **Scanner regression in Lab 2:** `ast_printer:src/scanner.py:99` no longer assigns True/False literals for keyword tokens. Lab 2 AST tests pass, but the earlier scanner contract test fails when run cumulatively. The `scanner` and later `parser` branches provide the expected literal values. This is a compatibility finding for the selected Python interfaces; the lab instructions themselves allow alternate language designs.

## Cumulative checks at every stage

| Through lab | Discovered checks (includes stage skips) | Failing checks |
|---|---:|---|
| `lab01_scanner` | 25 | None |
| `lab02_ast` | 34 | `test_literal_keyword_values` |
| `lab03_parser` | 59 | None |
| `lab04_interpreter` | 90 | `test_division_by_zero_is_language_error` |
| `lab05_variables` | 108 | `test_division_by_zero_is_language_error`, `test_assign_enclosing_variable`, `test_assignment`, `test_assignment_to_nearest_scope`, `test_print_and_expression_statements` |
| `lab06_control_flow` | 127 | `test_division_by_zero_is_language_error` |
| `lab07_functions` | 141 | `test_division_by_zero_is_language_error` |
| `lab08_resolver` | 154 | `test_division_by_zero_is_language_error` |
| `lab09_classes` | 167 | `test_division_by_zero_is_language_error` |
| `lab10_inheritance` | 179 | `test_division_by_zero_is_language_error` |

Reports, screenshots, custom grammar choices, and extra credit were not automatically graded. No instructor branch, solution file, or submission policy was changed.

## Reproduce

```sh
python3 tools/validate_branches.py ../mylox --output /tmp/cis343-matched.json
python3 tools/validate_branches.py ../mylox --cumulative --output /tmp/cis343-cumulative.json
```

The validator returns a nonzero status when the above reference defects are detected. This is expected; the tests do not suppress known failures.


## Harness and positive-path verification

All 22 maintenance tests pass, including release selection, cumulative stage
selection, malformed catalogs, case metadata, wrong outputs, wrong error types,
empty suites, and timeouts. Python syntax and workflow YAML were also checked.

As an additional control, only temporary copies of the reference snapshots were
corrected for the three findings above. The Lab 2 and Lab 5 cumulative suites
then passed, and the corrected `inheritance` snapshot passed all 175 applicable
checks (179 discovered, four superseded CLI checks skipped). These temporary
corrections were not applied to the instructor repository or included here.
This confirms that the tests can pass when the identified defects are corrected.
