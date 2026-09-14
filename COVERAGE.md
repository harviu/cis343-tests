# Requirement coverage

Source: the current local `labs_instruction/lab1.md`–`lab10.md`. Branch names and
exact validation commits are recorded in `VALIDATION.md`. This is the Python Lox
reference track selected for the course. No lab instructions were modified.

| Lab / suite | Reference branch | Checks | Automated coverage | Manual review / allowed variations |
|---|---|---:|---|---|
| 1 `lab01_scanner` | `scanner` | 25 | Token fields/display, all token categories, values, comments, line numbers, lexical errors, file/interactive plumbing, scanner CLI | Grammar design, screenshots covering the student's grammar, extensions |
| 2 `lab02_ast` | `ast_printer` | 9 | Fresh AST generation into a temporary directory, generated fields, printer nesting/operator order, exact assignment example | Formal grammar, metaprogramming approach, three report examples/screenshots |
| 3 `lab03_parser` | `parser` | 25 | Every specified operator, precedence/associativity, grouping, errors, scanner/parser/printer CLI | Concrete syntax tree and explanation, custom operators and grammar |
| 4 `lab04_interpreter` | `evaluater` | 31 | Arithmetic/comparisons, strings, unary operations, operand errors, division-by-zero error, calculator CLI | Semantic rules, evaluation-order explanation, non-boolean truthiness policy, approved extra credit |
| 5 `lab05_variables` | `statement` | 18 | Print/expression/declaration/assignment, environment API, nested scopes and assignment, exact textbook scope example, syntax errors and panic recovery | Redefinition/implicit-declaration choices, grammar, reports, optional static checks/initialization policies |
| 6 `lab06_control_flow` | `control_flow` | 19 | If/else, dangling else, while, nested loops, for clauses/scope, AST desugaring, missing parentheses/separators | Desugaring explanation, approved bare-declaration policy, optional break |
| 7 `lab07_functions` | `function_no_closure` | 14 | Calls, arity/type errors, native clock, declaration/parameters, all three return forms, nested calls/returns | Additional native functions, screenshots; closure is deferred to Lab 8 |
| 8 `lab08_resolver` | `resolver` | 13 | Closures and captured writes, all three assignment examples, environment distances, resolution errors | Explanation of binding differences and permitted resolution policies |
| 9 `lab09_classes` | `class` | 13 | Construction, separate instance fields, method access/binding, this/init, all required property/receiver errors | Checkpoint screenshots, optional static methods/getters |
| 10 `lab10_inheritance` | `inheritance` | 12 | Inherited/overridden methods, super dispatch and binding, initializers, all required super errors | Checkpoint screenshots and explanation |

**Total: 179 checks.** Individual-stage validation runs every check for that lab.
A full Lab 10 cumulative run discovers 179 checks and skips four obsolete CLI
checks (one from Lab 1, one from Lab 3, two from Lab 4). The underlying scanner,
AST, parser, and evaluator checks still run; Labs 5–10 exercise the current CLI.

Lab 2's generator test checks that executable classes are produced, rather than
only checking whether a generator file exists. Lab 6 checks actual `for` AST
lowering rather than accepting equivalent output as proof of desugaring. Lab 8
checks resolver distance callbacks in addition to execution examples.

Behavioral tests supplement, rather than replace, inspection of the required
algorithms. Language-design alternatives and extra credit can change baseline
expectations; use `CONTRACT.md` when deciding which tests apply to those students.
No extra credit is required by the default release list or baseline rubric.

The lab instructions still describe ZIP submission, while the GitHub template
proposes commit-link submission. Reconcile that course-policy text separately;
this test change does not alter submission instructions or grading percentages.
