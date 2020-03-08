# STANDARD
from pathlib import Path
import shutil
import os
import sys
import subprocess
import time

# PyPI
from click.testing import CliRunner
import pykeepass as keepass
import pytest

# LOCAL
from pykeypass import cli

test_dir = Path.cwd() / 'test'
test_database_no_key = test_dir / 'Database.kdbx'

# START CLICK PYTEST FUNCTIONALITY
runner = CliRunner()

# PREPARE TEST DATABASE
def test_setup():
    """Prepare environment for testing.

    Ensures that the following is not present:
    - Database.dbx does not contian 'new_entry'
    - test directory does not contain '.pykeypass'

    """
    if os.path.exists(test_dir / 'Database.kdbx'):
        kp = keepass.PyKeePass(test_dir / 'Database.kdbx', password='12345')
        entry = kp.find_entries(title=f'new_entry', first=True)
        if entry != None:
            kp.delete_entry('new_entry')
            entry = kp.find_entries(title=f'new_entry', first=True)
            assert entry == None
        else:
            assert entry == None
    else:
        assert False
    if os.path.exists(test_dir / '.pykeypass'):
        shutil.rmtree(test_dir / '.pykeypass')
    assert os.path.exists(test_dir / '.pykeypass') == False


def test_pykeypass_setup():
    """Test pykeypass setup."""
    result = runner.invoke(cli, ['setup', '-t'], input='12345')
    assert result.exit_code == 0
    assert not result.exception
    assert 'STEP 1: Create pykeypass app database.' in result.output
    assert ("DONE: pykeypass app database created.\n"
        + "Setup keepass databases by using:\n"
        + "- 'pykeypass open <new_name> -s'\n") in result.output


def test_pykeypass_setup_abort():
    response = runner.invoke(cli, ['setup', '-t'])
    assert response.exit_code != 0
    assert ('WARNING: If an app database already exists, this process '
        + 'will delete it and create a fresh one.\nProceed? (y/n) \n'
        + 'Aborted!\n') in response.output


def test_pykeypass_setup_again_replace():
    result = runner.invoke(cli, ['setup', '-t'], input='y\n12345\n')
    assert result.exit_code == 0
    assert 'STEP 1: Create pykeypass app database.' in result.output
    assert ("DONE: pykeypass app database created.\n"
        + "Setup keepass databases by using:\n"
        + "- 'pykeypass open <new_name> -s'\n") in result.output


def test_pykeypass_create_entry_no_key():
    result = runner.invoke(cli, ['open', 'new_entry', '-s', '-t'],
                           input=f'12345\n{test_database_no_key}\n12345\nn\n')
    assert result.exit_code == 0


def test_pykeypass_invalid_password():
    result = runner.invoke(cli, ['open', 'new_entry', '-t'], input='54321\n')
    assert 'ERROR: pykeypass login information invalid.\n' in result.output


def test_pykeypass_list_entries():
    result = runner.invoke(cli, ['open', '-o', '-t'], input='12345\n')
    assert result.exit_code == 0
    assert 'ENTRIES AVAILABLE: \nnew_entry' in result.output


def test_pykeypass_path_no_key():
    result = runner.invoke(cli, ['open', 'new_entry', '-p', '-t'], input='12345\n')
    assert str(test_database_no_key) in result.output


def test_pykeypass_path_no_key_replace():
    result = runner.invoke(cli, ['open', 'new_entry', '-s', '-t'],
                           input=f'12345\ny\n{test_database_no_key}\n12345\nn\n')
    assert result.exit_code == 0


def test_pykeypass_open_entry():
   result = runner.invoke(cli, ['open', 'new_entry', '-t'], input='12345\n')
   assert result.exit_code == 0


def test_pykeypass_all_basic():
    result = runner.invoke(cli, ['all', '-t'], input='12345\n')
    assert result.exit_code == 0
    assert f'STATUS: new_entry keypass database launched successfully.' in result.output


@pytest.mark.flaky(reruns=5, reruns_delay=2)
def test_teardown_install_files():
    time.sleep(2)
    pipe_local = subprocess.Popen('taskkill /IM Keepass.exe', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    if os.path.exists(test_dir / '.pykeypass'):
        shutil.rmtree(test_dir / '.pykeypass')
    assert os.path.exists(test_dir / '.pykeypass') == False
    if os.path.exists(test_dir / 'Database.kdbx'):
        kp = keepass.PyKeePass(test_dir / 'Database.kdbx', password='12345')
        entry = kp.find_entries(title=f'new_entry', first=True)
        if entry != None:
            kp.delete_entry('new_entry')
            entry = kp.find_entries(title=f'new_entry', first=True)
            assert entry == None
        else:
            assert entry == None
