from click.testing import CliRunner
from theseus.cli import run
from pathlib import Path

import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    runner = CliRunner()
    path = Path(__file__).parent
    os.chdir(path)
    input_file = path / 'configs' / 'to_be_confirmed' / 'heraldedW.json'
    logging.info(input_file)
    result = runner.invoke(run, [str(input_file)], catch_exceptions=False)
    print(result.output)