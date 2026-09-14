from pathlib import Path
from support import install_program_cases

install_program_cases(globals(), Path(__file__).with_name("cases.json"))
