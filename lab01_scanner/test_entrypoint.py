from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from error_handler import ErrorHandler
from lox import Lox


class EntryPointTests(unittest.TestCase):
    def setUp(self):
        ErrorHandler.had_error = False
        ErrorHandler.had_runtime_error = False

    def test_file_mode_reads_source(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'source.lox'
            path.write_text('print "hello";')
            interpreter = Lox()
            with patch.object(interpreter, 'run') as run:
                interpreter.run_file(str(path))
                run.assert_called_once_with('print "hello";')

    def test_interactive_mode_passes_input_to_run(self):
        interpreter = Lox()
        with patch('builtins.input', side_effect=['print 1;', KeyboardInterrupt]), \
                patch.object(interpreter, 'run') as run, redirect_stdout(io.StringIO()):
            interpreter.run_prompt()
            run.assert_called_once_with('print 1;')
