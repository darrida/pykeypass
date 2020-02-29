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
#######################################


@click.group()
def cli():
    '''KEEPASS CLI TOOL
    
    This tool can be configured to launch any number of Keepass databases with a single command (and password).
    '''


@cli.command('setup', help='Initial setup of pykeypass app database.')
def pykeypass_setup():        
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


@cli.command('open', help='Launches specified Keepass database.')
@click.argument('database', required=False)
@click.option('-s', '--setup', 'setup', is_flag=True, help='Add or replace a named Keepass database')
@click.option('-p', '--path', 'path', is_flag=True, help='Show named Keepass path')
@click.option('-i', '--input_password', 'input_password', help="reserved for use with 'pykeepass all'")
@click.option('-o', '--options', 'options', is_flag=True, help='Lists Keypass databases available')
def keepass_open(database, setup, path, options, input_password=None):
    try:
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
            #try:
            kp = PyKeePass(pykeypass_db, password=getpass.getpass('pykeypass password: '))
            groups = kp.find_groups(name='.', regex=True)
            click.echo('The "open" command launches the specified Keepass database entry in it\'s argument.\n\nENTRIES AVAILABLE: ')
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
                click.echo(f'ISSUE: All or part of the {database} Keepass entry was not found.\nFIX: Setup this entry using: "pykeypass open {database} -s')
        else:
            try:
                password = getpass.getpass('pykeepass password: ') if input_password == None else input_password
                kp = keepass.PyKeePass(pykeypass_db, password=password)
                entry = kp.find_entries(title=f'{database}', first=True)
                print(entry)
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
                    click.echo(f'ISSUE: All or part of the {database} Keepass entry was not found.\nFIX: Setup this entry using: "pykeypass open {database} -s')
                elif str(e) == "'NoneType' object has no attribute 'password'":
                    click.echo(f'ISSUE: It looks like there is no password configured for the {database} Keepass database.')
                else:
                    click.echo(f'Error message: {e}')
            except subprocess.CalledProcessError as e:
                click.echo(e)
    except FileNotFoundError as e:
        click.echo("ERROR: pykeepass app database not found. Use 'pykeypass setup' to get started.\n")


@cli.command('all', help='Starts all configured keepass databases.')
def keepass_all():
    try:
        password = getpass.getpass('pykeepass password: ')
        kp = PyKeePass(pykeypass_db, password=password)
        groups = kp.find_groups(name='.', regex=True)
        for i in groups[1:]:
            database_entry = str(i)[8:-2]
            pipe_local = subprocess.Popen(f'pykeypass open {database_entry} -i {password}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if pipe_local.communicate():
                if pipe_local.returncode == 0:
                    click.echo(f'STATUS: {database_entry} keypass database launched successfully.')
    except subprocess.CalledProcessError as e:
        click.echo(e)
