# Standard
import os
from pathlib import Path
import getpass
import subprocess
import shutil

# PYPI
import click
from pykeepass import PyKeePass
import pykeepass as keepass


########## GLOBAL VARIABLES ###########
pykeypass_folder = Path.home() / '.pykeypass'
pykeypass_app = pykeypass_folder / 'keepass.exe'
pykeypass_db = pykeypass_folder / 'pykeepass.kdbx'
########## PYTEST VARIABLES ###########
test_pykeypass_folder = Path.cwd() / 'test' / '.pykeypass'


def path_selection(test=False):
    pykeypass_folder = (Path.home() / '.pykeypass' if test == False else Path.cwd() / 'test' / '.pykeypass')
    pykeypass_app = pykeypass_folder / 'keepass.exe'
    pykeypass_db = pykeypass_folder / 'pykeepass.kdbx'
    return pykeypass_folder, pykeypass_app, pykeypass_db


@click.group()
def cli():
    '''KEEPASS CLI TOOL
    
    This tool can be configured to launch any number of Keepass databases with a single command (and password).
    '''


@cli.command('setup', help='Initial setup of pykeypass app database.')
@click.option('-t', '--test', 'test', is_flag=True, hidden=True)
def pykeypass_setup(test):
    """Intial setup

    - Copies Keepass.exe to .pykeypass folder in home directory
    - Creates pykeypass.kdbx in .pykeypass folder in hom directory
    """
    try:
        pykeypass_folder, pykeypass_app, pykeypass_db = path_selection(test)
        if os.path.exists(pykeypass_app) == False:
            Path(pykeypass_folder).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path.cwd() / 'thirdparty' / 'keepass_portable' / 'keepass.exe', pykeypass_app)
        if os.path.exists(pykeypass_db):
            confirmation = input('WARNING: If an app database already exists, this process will delete it and create a fresh one.\nProceed? (y/n) ')
        else:
            confirmation = 'y'
        if confirmation == 'y':
            click.echo('STEP 1: Create pykeypass app database.')
            new_password = getpass.getpass('Create a pykeypass password: ')
            keepass.create_database(pykeypass_db, password=new_password)
            kp = PyKeePass(pykeypass_db, password=new_password)
            click.echo("DONE: pykeypass app database created.\n"
                    "Setup keepass databases by using:\n"
                    "- 'pykeypass open <new_name> -s'\n")
        else:
            click.echo('pykeypass setup cancelled.')
    except FileNotFoundError as e:
        click.echo("""ERROR: pykeypass app not setup. To setup, perform one of the following:
(1) Run 'install.bat' from pykeypass app folder.
(2) Open CMD/terminal in root of pykeypass app directory and run 'pykeypass setup' (all other functionality is global)""")


@cli.command('open', help='Launches functionality for a specific Keepass database.')
@click.argument('database', required=False)
@click.option('-s', '--setup', 'setup', is_flag=True, help='Add or replace the requsested database entry')
@click.option('-p', '--path', 'path', is_flag=True, help='Show path(s) associated with requested database entry')
@click.option('-i', '--input_password', 'input_password', help="Reserved for use with 'pykeepass all'")
@click.option('-o', '--options', 'options', is_flag=True, help='Lists Keypass database entries available')
@click.option('-t', '--test', 'test', is_flag=True, hidden=True)
def keepass_open(database, setup, path, options, test, input_password=None):
    """Launches functionality for specified Keepass database.

    When no argument is provided, function defaults to the 'options' flag.

    Args:
        database (string):                 Launches specific database entry when no options are used.
        setup (boolean):                   When used, launches setup wizard for database entry. Defaults to False.
        path (boolean):                    When used, shows file(s) for database entry. Defaults to False.
        options (boolean):                 When used, shows list of all database entries available. Defaults to False.
        input_password (string, optional): Designed for use by the keepass_all() function further below. Defaults to None.
    """
    try:
        pykeypass_folder, pykeypass_app, pykeypass_db = path_selection(test)
        if database == None:
            options = True
        if setup:
            try:
                click.echo(f'START: Setup {database} keepass.')
                password = getpass.getpass('pykeypass password: ')
                kp = PyKeePass(pykeypass_db, password=password)
                group = kp.find_groups(kp.root_group, f'{database}')
                entry = kp.find_entries(title=f'{database}', first=True)
                if entry != None:
                    confirmation = input(f'WARNING: An entry for {database} already exists, this process will delete it and create a fresh one.\nProceed? (y/n) ')
                    kp.delete_entry(entry)
                    kp.delete_group(group)
                    kp.save()
                else:
                    confirmation = 'y'
                if confirmation == 'y':
                    kp = PyKeePass(pykeypass_db, password=password)
                    keepass_url = input(f'Set {database} Keepass url: ')
                    keepass_pw = getpass.getpass(f'Set {database} Keepass Password: ')
                    group = kp.add_group(kp.root_group, f'{database}')
                    kp.add_entry(group, f'{database}', f'{database}', keepass_pw, url=keepass_url)
                    kp.save()
                    key_question = input('Does this Keepass database use a key file? (y/n) ')
                    if key_question == 'y':
                        kp = PyKeePass(pykeypass_db, password=password)
                        entry = kp.find_entries(title=f'{database}', first=True)
                        key_file = input('Set key file (file path + file name): ')
                        entry.set_custom_property('key', str(key_file))
                kp.save()
                click.echo(f'DONE: {database} keepass password setup.')
                click.echo(f'Try launching with "pykeypass open {database}", or "pykeypass all"')
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
        elif options:
            kp = PyKeePass(pykeypass_db, password=getpass.getpass('pykeypass password: '))
            groups = kp.find_groups(name='.', regex=True)
            click.echo('ENTRIES AVAILABLE: ')
            for i in groups[1:]:
                if str(i)[8:-2] != 'Recycle Bin':
                    print(str(i)[8:-2])
        elif path:
            try:
                kp = PyKeePass(pykeypass_db, password=getpass.getpass('pykeypass password: '))
                entry = kp.find_entries(title=f'{database}', first=True)
                click.echo(f'{database.upper()} PATH: {entry.url}')
                if entry.get_custom_property('key'):
                    key_name = entry.get_custom_property('key')
                    click.echo(f'{database.upper()} KEY: {key_name}')
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
            except AttributeError as e:
                click.echo(f'ISSUE: All or part of the {database} Keepass entry was not found.\nFIX: Setup this entry using: "pykeypass open {database} -s"')
        else:
            try:
                password = getpass.getpass('pykeepass password: ') if input_password == None else input_password
                kp = keepass.PyKeePass(pykeypass_db, password=password)
                entry = kp.find_entries(title=f'{database}', first=True)
                if entry.get_custom_property('key') != None:
                    key_file = entry.get_custom_property('key')
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password} -keyfile:"{key_file}"',
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password}', 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
            except AttributeError as e:
                click.echo(f'ERROR: Setup item for {database} file missing or incorrect')
                if str(e) == "'NoneType' object has no attribute 'url'":
                    click.echo(f'ISSUE: It looks like there is no url configured for the {database} Keepass database.')
                elif entry == None:
                    click.echo(f'ISSUE: All or part of the {database} Keepass entry was not found.\nFIX: Setup this entry using: "pykeypass open {database} -s"')
                #elif str(e) == "'NoneType' object has no attribute 'password'":
                #    click.echo(f'ISSUE: It looks like there is no password configured for the {database} Keepass database.')
                else:
                    click.echo(f'Error message: {e}')
            except subprocess.CalledProcessError as e:
                click.echo(e)
    except FileNotFoundError as e:
        click.echo("ERROR: pykeepass app database not found. Use 'pykeypass setup' to get started.\n")


@cli.command('all', help='Starts all configured Keepass databases.')
@click.option('-t', '--test', 'test', is_flag=True, hidden=True)
def keepass_all(test):
    """Launches all database entries
    """
    try:
        mode = ('-t' if test == True else '')
        pykeypass_folder, pykeypass_app, pykeypass_db = path_selection(test)
        password = getpass.getpass('pykeepass password: ')
        kp = PyKeePass(pykeypass_db, password=password)
        groups = kp.find_groups(name='.', regex=True)
        if len(groups) > 1:
            for i in groups[1:]:
                database_entry = str(i)[8:-2]
                pipe_local = subprocess.Popen(f'pykeypass open {database_entry} -i {password} {mode}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if pipe_local.communicate():
                    if pipe_local.returncode == 0:
                        click.echo(f'STATUS: {database_entry} keypass database launched successfully.')
        else:
            click.echo('NOTICE: No entry created. Use \'pykeypass open <new_name> -s\''
                + 'to get started.')
    except FileNotFoundError:
        click.echo('ERROR: pykeepass app database not found. Use \'pykeypass setup\' to get started.\n')
    except subprocess.CalledProcessError as e:
        click.echo(e)
