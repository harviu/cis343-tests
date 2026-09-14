# CIS343 released practice tests

Instructor-maintained tests and a reusable GitHub Actions workflow for the
[student template](https://github.com/harviu/cis343-student-template).
Only Lab 1 (22 scanner/token checks) is released initially. Python 3.12 and Git
are sufficient; no third-party test framework is required.

This public repository contains practice tests, not instructor solutions or
hidden final-grading tests. Only the instructor and TAs should have write access.

## How updates reach students

Student repositories call `.github/workflows/grade.yml@main`. Every fresh run
fetches `main`, reads `released_labs.json`, and creates one job per released lab.
All jobs in that run use the same recorded test commit. Updates to this workflow
and test repository take effect on the next student push or manual workflow run.
A test update alone does not trigger runs in all student repositories.

For local feedback, students run `python3 scripts/test.py` in their repository;
it downloads the current tests into a temporary directory each time.

## Release a new lab

1. Add a directory such as `lab02_ast/` with Python `unittest` files named
   `test_*.py`. Import student modules using the interfaces in `CONTRACT.md`.
2. Validate against a correct implementation and deliberately broken versions.
3. Update `CONTRACT.md` to document the new public interface.
4. Append the directory name to `released_labs.json`, keeping previous labs:

   ```json
   ["lab01_scanner", "lab02_ast"]
   ```

5. Commit and push to `main`. Student repositories need no edits.

Write unreleased tests privately if students should not see them. A branch in a
public repository is still public. A directory is only executed after it appears
in the release list. Invalid manifests, empty suites, failures, and timeouts
return failure rather than a successful check.

## Run manually

```sh
python3 run_tests.py /path/to/student-repository
python3 run_tests.py /path/to/student-repository --lab lab01_scanner
python3 run_tests.py --list
python3 -m unittest discover -s harness_tests -v
```

The runner allows 120 seconds per suite by default and continues to subsequent
labs after a failure. GitHub adds a five-minute maximum to each lab job. Individual
checks are visible in the logs. The current checks target the Python Lox reference
interfaces; see [CONTRACT.md](CONTRACT.md) for exact behavior and coverage limits.

## Reproducible final grading

For each submission, record the student commit and test commit. To reproduce a
past result, check out those two commits and run `run_tests.py` directly instead
of the student's command that fetches the latest release. Freeze the chosen test
commit for a grading round so changing practice tests does not silently change
past grades.

Student repository checks are feedback, not tamper-proof grades: students can
edit their caller workflow or code. Run final checks in an instructor-controlled,
isolated process without exposing instructor credentials to student code. Keep
hidden grading tests outside this public repository. Reports, design decisions,
CLI behavior, and readability still require review against the course rubric.

## Maintenance checks

The repository's `Validate test harness` workflow checks release configuration,
Python syntax, and runner behavior (passing/failing/empty suites and timeouts).
It does not contain a reference solution or certify every released lab test.
Before releasing new tests, also run them against your private reference solution.
