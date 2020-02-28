# Standard
import os
#import sys
from pathlib import Path
import getpass
import subprocess
import shutil
from shutil import copyfile

#import time

# PYPI
import click
from pykeepass import PyKeePass
import pykeepass as keepass

########################################
########## DECLARE VARIABLES ###########
########################################
# network Keepass
path_db_network = Path('C:/<path>/')
file_db_network = '<network_name>.kdbx'
path_key_network = Path('C:/<path>/')
file_key_network = '<network_name>.key'
#key_file = Path.home() / 'file.key'
# Personal Keepass
path_db_local = ''
file_db_local = ''
path_key_local = ''
file_key_local = ''
# App General
pykeypass_folder = Path.home() / 'pykeypass_app_files'
pykeypass_app = pykeypass_folder / 'keepass.exe'
pykeypass_db = pykeypass_folder / 'pykeepass.kdbx'
#######################################


@click.group()
def cli():
    '''KEEPASS CLI TOOL'''


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
        new_password = getpass.getpass('pykeypass password: ')
        keepass.create_database(pykeypass_db, password=new_password)
        kp = PyKeePass(pykeypass_db, password=new_password)
        click.echo("DONE: pykeypass app database created.\n"
                   "Setup keepass files by using:\n"
                   "- 'pykeypass network -s'\n"
                   "- 'pykeypass local -s'\n")
    else:
        click.echo('pykeypass setup cancelled.')


@cli.command('network', help='Launches network Keepass database.')
@click.option('-s', '--setup', 'setup', is_flag=True, help='Setup storage of network Keepass password')
@click.option('-p', '--path', 'path', is_flag=True, help='Show network Keepass path')
@click.option('-i', '--input_password', 'input_password', help="reserved for use with 'pykeepass all'")
def keepass_network(path, setup, input_password=None):
    try:
        if setup:
            try:
                click.echo('START: Setup network keepass.')
                password = getpass.getpass('pykeypass password: ')
                kp = PyKeePass(pykeypass_db, password=password)
                group = kp.find_groups(kp.root_group, 'network')
                entry = kp.find_entries(title='network_file', first=True)
                if entry != None:
                    confirmation = input('WARNING: An entry for network already exists, this process will delete it and create a fresh one.\nProceed? (y/n) ')
                    kp.delete_entry(entry)
                    kp.delete_group(group)
                    kp.save()
                else:
                    confirmation = 'y'
                if confirmation == 'y':
                    kp = PyKeePass(pykeypass_db, password=password)
                    network_url = input('Set network Keepass url: ')
                    network_keepass_pw = getpass.getpass('Set network Keepass Password: ')
                    group = kp.add_group(kp.root_group, 'network')
                    kp.add_entry(group, 'network_file', 'network', network_keepass_pw, url=network_url)
                    kp.save()
                    key_question = input('Does this Keepass database use a key file? (y/n) ')
                    if key_question == 'y':
                        kp = PyKeePass(pykeypass_db, password=password)
                        entry = kp.find_entries(title='network_file', first=True)
                        key_file = input('Set key file (file path + file name): ')
                        entry.set_custom_property('key', str(key_file))
                kp.save()
                click.echo('DONE: network keepass password setup.')
                click.echo('Try launching with "pykeepass network"')
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
        elif path:
            try:
                kp = PyKeePass(pykeypass_db, password=getpass.getpass('pykeypass password: '))
                entry = kp.find_entries(title='network_file', first=True)
                click.echo(f'network PATH: {entry.url}')
                if entry.get_custom_property('key'):
                    print(str(entry.get_custom_property('key')))
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
        else:
            try:
                password = getpass.getpass('pykeepass password: ') if input_password == None else input_password
                kp = keepass.PyKeePass(pykeypass_db, password=password)
                entry = kp.find_entries(title='network_file', first=True)
                if entry.get_custom_property('key'):
                    key_file = entry.get_custom_property('key')
                    print(entry.url)
                    print(key_file)
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password} -keyfile:"{key_file}"',
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    print(entry.url)
                    print(pykeypass_app)
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password}', 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
            except AttributeError as e:
                click.echo(f'ERROR: Setup item for local file missing or incorrect')
                if str(e) == "'NoneType' object has no attribute 'url'":
                    click.echo('ISSUE: It looks like there is no url configured for the local Keepass database.')
                elif str(e) == "'NoneType' object has no attribute 'password'":
                    click.echo('ISSUE: It looks like there is no password configured for the local Keepass database.')
                else:
                    click.echo(f'Error message: {e}')
            except subprocess.CalledProcessError as e:
                click.echo(e)
    except FileNotFoundError as e:
        click.echo("ERROR: pykeepass app database not found. Use 'pykeypass setup' to get started.\n")


@cli.command('local', help='Launches local Keepass database.')
@click.option('-s', '--setup', 'setup', is_flag=True, help='Facilitates configuring local keepass file')
@click.option('-p', '--path', 'path', is_flag=True, help='Show local Keepass path')
@click.option('-i', '--input_password', 'input_password', help="reserved for use with 'pykeepass all'")
def keepass_local(setup, path, input_password=None):
    try:
        if setup:
            try:
                click.echo('START: Setup local keepass.')
                password = getpass.getpass('pykeypass password: ')
                kp = PyKeePass(pykeypass_db, password=password)
                group = kp.find_groups(kp.root_group, 'local')
                entry = kp.find_entries(title='local_file', first=True)
                if entry != None:
                    confirmation = input('WARNING: An entry for local already exists, this process will delete it and create a fresh one.\nProceed? (y/n) ')
                    kp.delete_entry(entry)
                    kp.delete_group(group)
                    kp.save()
                else:
                    confirmation = 'y'
                if confirmation == 'y':
                    kp = PyKeePass(pykeypass_db, password=password)
                    local_url = input('Set local Keepass url: ')
                    local_keepass_pw = getpass.getpass('Set local Keepass Password: ')
                    group = kp.add_group(kp.root_group, 'local')
                    kp.add_entry(group, 'local_file', 'local', local_keepass_pw, url=local_url)
                    kp.save()
                    key_question = input('Does this Keepass database use a key file? (y/n) ')
                    if key_question == 'y':
                        kp = PyKeePass(pykeypass_db, password=password)
                        entry = kp.find_entries(title='local_file', first=True)
                        key_file = input('Set key file (file path + file name): ')
                        entry.set_custom_property('key', str(key_file))
                kp.save()
                click.echo('DONE: local keepass password setup.')
                click.echo('Try launching with "pykeepass local"')
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
        elif path:
            try:
                kp = PyKeePass(pykeypass_db, password=getpass.getpass('pykeypass password: '))
                entry = kp.find_entries(title='local_file', first=True)
                click.echo(f'LOCAL PATH: {entry.url}')
                if entry.get_custom_property('key'):
                    print(str(entry.get_custom_property('key')))
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
        else:
            try:
                password = getpass.getpass('pykeepass password: ') if input_password == None else input_password
                kp = keepass.PyKeePass(pykeypass_db, password=password)
                entry = kp.find_entries(title='local_file', first=True)
                if entry.get_custom_property('key'):
                    key_file = entry.get_custom_property('key')
                    print(entry.url)
                    print(key_file)
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password} -keyfile:"{key_file}"',
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    print(entry.url)
                    print(pykeypass_app)
                    subprocess.Popen(f'{pykeypass_app} "{entry.url}" -pw:{entry.password}', 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except keepass.exceptions.CredentialsIntegrityError as e:
                click.echo('ERROR: pykeypass login information invalid.\n')
            except AttributeError as e:
                click.echo(f'ERROR: Setup item for local file missing or incorrect')
                if str(e) == "'NoneType' object has no attribute 'url'":
                    click.echo('ISSUE: It looks like there is no url configured for the local Keepass database.')
                elif str(e) == "'NoneType' object has no attribute 'password'":
                    click.echo('ISSUE: It looks like there is no password configured for the local Keepass database.')
                else:
                    click.echo(f'Error message: {e}')
            except subprocess.CalledProcessError as e:
                click.echo(e)
    except FileNotFoundError as e:
        click.echo("ERROR: pykeepass app database not found. Use 'pykeypass setup' to get started.\n")


@cli.command('all', help='Starts all keepass database.')
def keepass_all():
    try:
        password = getpass.getpass('pykeepass password: ')
        pipe_local = subprocess.Popen(f'pykeypass local -i {password}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if pipe_local.communicate():
            if pipe_local.returncode == 0:
                click.echo('STATUS: Local keypass database launched successfully.')
        pipe_network = subprocess.Popen(f'pykeypass network -i {password}', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if pipe_network.communicate():
            if pipe_network.returncode == 0:
                click.echo('STATUS: Network keypass database launched successfully.')
    except subprocess.CalledProcessError as e:
        click.echo(e)
