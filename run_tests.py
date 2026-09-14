"""Run the released instructor suites against a supplied student checkout."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def released_labs(root=ROOT):
    labs = json.loads((root / "released_labs.json").read_text())
    if (not isinstance(labs, list) or not labs
            or any(not isinstance(lab, str) or not re.fullmatch(r"lab[0-9]{2}_[a-z0-9_]+", lab) for lab in labs)
            or len(set(labs)) != len(labs)):
        raise ValueError("released_labs.json must contain distinct lab directory names")
    for lab in labs:
        if not list((root / lab).glob("test_*.py")):
            raise ValueError(f"Released lab {lab} has no test_*.py files")
    return labs


def run_lab(project, lab, timeout, root=ROOT):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project / "src")
    env["CIS343_STUDENT_ROOT"] = str(project)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Discovery and execution are isolated in a child process. An empty suite
    # is an error, rather than unittest's default successful zero-test result.
    code = """import sys, unittest
suite = unittest.defaultTestLoader.discover(sys.argv[1], pattern='test_*.py')
if suite.countTestCases() == 0:
    print('ERROR: no tests discovered', file=sys.stderr)
    sys.exit(2)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
"""
    try:
        return subprocess.run(
            [sys.executable, "-c", code, str(root / lab)],
            cwd=root, env=env, timeout=timeout, check=False,
        ).returncode
    except subprocess.TimeoutExpired:
        print(f"FAIL: {lab} exceeded {timeout} seconds", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", type=Path)
    parser.add_argument("--lab", help="Run one released lab")
    parser.add_argument("--list", action="store_true", help="Print released labs as JSON")
    parser.add_argument("--timeout", type=float, default=120, help="Seconds allowed per lab")
    args = parser.parse_args()
    try:
        labs = released_labs()
        if args.list:
            print(json.dumps(labs))
            return 0
        if args.project is None or not (args.project / "src").is_dir():
            parser.error("project must contain a src directory")
        if args.timeout <= 0:
            parser.error("timeout must be positive")
        if args.lab:
            if args.lab not in labs:
                parser.error(f"Lab is not released: {args.lab}")
            labs = [args.lab]
        revision = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                  capture_output=True, text=True, check=False)
        print("Test commit:", revision.stdout.strip() or "local uncommitted copy", flush=True)
        failed = False
        for lab in labs:
            print(f"\n=== {lab} ===", flush=True)
            status = run_lab(args.project.resolve(), lab, args.timeout)
            print(f"{lab}: {'PASS' if status == 0 else 'FAIL'}", flush=True)
            failed = failed or status != 0
        return 1 if failed else 0
    except (ValueError, OSError) as error:
        print(f"Test configuration error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
