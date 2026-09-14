# CIS343 cumulative lab tests

Practice tests for all ten Python Lox labs, based on `labs_instruction/lab1.md`
through `lab10.md` and the corresponding local `mylox` branches. The 179 named
checks cover both individual lab requirements and cumulative behavior.
Python 3.12+ and Git are required; no third-party test framework is needed.

**Only Lab 1 is currently released.** Labs 2–10 can be previewed locally with an
explicit flag and do not join student Actions runs until added to the release
list. Files pushed to this public repository are visible even when unreleased.

- [Coverage and manual-review requirements](COVERAGE.md)
- [Python interfaces and baseline policies](CONTRACT.md)
- [Reference branch validation and known failures](VALIDATION.md)
- [Branch mapping](lab_branches.json)

## Run tests

From this `cis343-tests` directory:

```sh
# Run currently released tests against a student checkout.
python3 run_tests.py ../cis343-student-template

# Preview a single unreleased lab against a checkout implementing that lab.
python3 run_tests.py /path/to/student-checkout --lab lab02_ast --include-unreleased

# Preview all cumulative checks through Lab 8.
python3 run_tests.py /path/to/student-checkout --through lab08_resolver --include-unreleased

# List current release or the complete instructor catalog.
python3 run_tests.py --list
python3 run_tests.py --list --include-unreleased
```

`--include-unreleased` is a local selection option, not a security mechanism.
Do not put it in the shared student workflow. Keep released labs in course order.
With the default workflow, the last released lab determines the current CLI
stage. Explicit instructor previews use `--lab` or `--through` as that stage.
Historical CLI output checks for Labs 1, 3, and 4 are skipped once superseded;
all their API checks remain active. Every later program suite checks the real CLI.

Each program has a five-second timeout. Each lab has a 120-second limit; the
runner continues to subsequent labs after failure. GitHub limits each job to
five minutes. Individual checks and diagnostics appear in the log.

## Validate against your branches

```sh
# Each lab's own suite against its mapped reference branch.
python3 tools/validate_branches.py ../mylox --output /tmp/cis343-matched.json

# All previous suites as well, at every stage.
python3 tools/validate_branches.py ../mylox --cumulative --output /tmp/cis343-cumulative.json
```

The validator archives committed local branch snapshots into temporary folders.
It does not switch branches, edit solutions, use uncommitted changes, or fetch
from GitHub. It records each commit and writes per-lab logs beside the output
file. An exit code of 1 means at least one reference did not pass; known findings
are documented in `VALIDATION.md`. No reference solutions are stored here.

## Release a lab to students

1. Review its cases and policies, validate against the intended reference, and
   resolve or account for findings in `VALIDATION.md`.
2. Append the suite to `released_labs.json`, preserving earlier suites, for example:

   ```json
   ["lab01_scanner", "lab02_ast"]
   ```

3. Commit and push the test files and release list to `main`.

Student repositories use `harviu/cis343-tests/.github/workflows/grade.yml@main`.
Every fresh push/manual run fetches the release list and starts a separate job
for each lab, using one test commit for the whole run. Editing tests alone does
not trigger every student's workflow. The student command `python3 scripts/test.py`
also downloads current tests before running them.

The runner, shared support module, catalog, and suite files must be published
together. For a future release that must stay hidden until its start date, keep
the files locally or in a private instructor repository until then.

## Add or change cases

For Labs 5–10, edit the corresponding `cases.json`. Use a unique `name`, the Lox
`source`, a `requirement` description, and either an `output` list or an `error`
regular expression. Expected numbers and booleans are JSON values; strings are
literal output lines. Every case becomes its own named unittest.

API suites use Python `unittest` and the interfaces in `CONTRACT.md`.
Run maintenance checks after editing:

```sh
python3 -m unittest discover -s harness_tests -v
```

The maintenance workflow checks syntax, catalog/case configuration, selection,
and runner behavior. It does not certify reference solutions or replace
validation of new test expectations against the lab instructions.

## Final grading

Record the student commit and test commit. Freeze a test version for each grading
round, and check out those exact commits to reproduce results. Practice checks
in student repositories are editable by students; final grading needs an
instructor-controlled isolated process. Keep hidden tests and credentials away
from student-controlled workflows. Review reports and the rest of the rubric
separately. Passing the practice checks alone is not a complete grade.
