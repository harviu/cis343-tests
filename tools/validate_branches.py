"""Validate local mylox branch snapshots without checking out or changing branches."""
import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path, help='Local mylox Git repository')
    parser.add_argument('--cumulative', action='store_true', help='Run all suites through each stage')
    parser.add_argument('--output', type=Path, help='Write JSON results and per-lab logs next to this file')
    args = parser.parse_args()
    results = []
    mapping = json.loads((ROOT / 'lab_branches.json').read_text())
    with tempfile.TemporaryDirectory(prefix='cis343-reference-') as temp:
        for lab, branch in mapping.items():
            entry = {'lab': lab, 'branch': branch}
            try:
                sha = subprocess.check_output(['git', '-C', str(args.repository.resolve()),
                                               'rev-parse', '--verify', f'refs/heads/{branch}^{{commit}}'], text=True).strip()
                data = subprocess.check_output(['git', '-C', str(args.repository.resolve()), 'archive', sha])
                checkout = Path(temp) / branch
                checkout.mkdir()
                with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                    # Supported by Python 3.12+; rejects paths outside destination.
                    archive.extractall(checkout, filter='data')
                command = [sys.executable, str(ROOT / 'run_tests.py'), str(checkout),
                           '--through' if args.cumulative else '--lab', lab, '--include-unreleased']
                run = subprocess.run(command, capture_output=True, text=True, timeout=1300)
                log = run.stdout + run.stderr
                counts = [int(n) for n in re.findall(r'^Ran (\d+) tests?', log, re.M)]
                failed = re.findall(r'^(?:FAIL|ERROR): (.+)$', log, re.M)
                entry.update(commit=sha, tests=sum(counts), returncode=run.returncode, failures=failed)
                if args.output:
                    args.output.parent.mkdir(parents=True, exist_ok=True)
                    log_path = args.output.parent / (args.output.stem + '-' + lab + '.log')
                    log_path.write_text(log)
            except (OSError, subprocess.SubprocessError, tarfile.TarError) as error:
                entry.update(returncode=2, error=str(error))
            results.append(entry)
            print(json.dumps(entry), flush=True)
    if args.output:
        args.output.write_text(json.dumps(results, indent=2) + '\n')
    return int(any(item['returncode'] for item in results))


if __name__ == '__main__':
    sys.exit(main())
