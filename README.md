[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
![alt text][coverage]
![windows](https://img.shields.io/badge/Windows-0078D6)

[coverage]: https://github.com/darrida/pykeypass/blob/master/coverage.svg "testing coverage"

# pykeypass

pykeypass (because pykeepass was already taken) uses the pykeepass library to setup to specify and quickly launch multiple Keepass databases

**Table of Contents**

- [pykeypass](#pykeypass)
  - [Background](#background)
  - [Setup](#setup)
  - [Usage](#usage)
    - [Setup standalone Keepass executable and app database:](#setup-standalone-keepass-executable-and-app-database)
    - [Setup a new Keypass database entry](#setup-a-new-keypass-database-entry)
    - [Open individual Keepass database](#open-individual-keepass-database)
    - [Show list of configured databases](#show-list-of-configured-databases)
    - [Show path of individual configured database](#show-path-of-individual-configured-database)
  - [Testing](#testing)

## Background

This is a tool that I use almost everyday, both at home and at work. 

**THE PROBLEM:**
At work I typically have 2-3 different Keepass databases open at the same time. This means that after I arrived on any given day one of the first things I would do is open Keypass. After that I would proceed to open the "File" menu, select the first item out of the recents section, and input the password. Then, again, I'd open the "File" menu and repeat the same set of steps a couple of more times. 

Occassionally I'd find that something cleared out the recents options, which means that I would have to manually browse to the different network directory locations where each Keepass database lived to open them.

**THE SOLUTION:**
pykeypass allows me to open the Command Prompt, type ```pykeypass all```, input a single password, then sit back and watch all of my Keypass databases open programmatically.

## Setup

### Requiremements
- This utlity is build for Windows
- Python 3.9 - 3.12 supported

### Install
- Standard

```
pip install pykeypass
```

- **pipx** Recommended

```
pipx install pykeypass
```

## Usage

### Setup standalone Keepass executable and app database:

- **NOTE:** Initial setup of pykeypass database should take place during the setup above. The process below can be used to re-setup the pykeypass database
```cmd
pykeypass setup
```

- Input password when directed.
- If the setup completes successfully, the following will appear:

```cmd
DONE: pykeypass app database created.
Setup keepass databases by using:
- 'pykeypass open <new_name> -s'
```

- **NOTE:** If a pykeypass app database already exists an additional prompt will appear with a warning that proceeding will delete the current database and create a new one.

### Setup a new Keypass database entry

```cmd
pykeypass manage <new_entry>
```

- pykeypass will walk through the following:
  - (1) Specifying the new Keepass database url
  - (2) Specifying the password
  - (3) Whether or not the Keepass database uses a paired security key
- Standard Example:

```cmd
C:\> pykeypass manage <new_entry>
START: Setup database_with_key keepass.
pykeypass password:
Set new_entry Keepass url: C:\Users\<user>\Documents\database.kdbx
Set new_entry Keepass Password:
Does this Keepass database use a key file? (y/n) n
DONE: local keepass password setup.
Try launching with "pykeepass open local"
```

- Example with paired security key:

```cmd
C:\> pykeypass manage <new_entry>
START: Setup database_with_key keepass.
pykeypass password:
Set database_with_key Keepass url: C:\Users\<user>\Documents\database.kdbx
Set database_with_key Keepass Password:
Does this Keepass database use a key file? (y/n) y
Set key file (file path + file name): C:\Users\<user>\Documents\database.key
DONE: database_with_key keepass password setup.
Try launching with "pykeypass open database_with_key"
```

### Open individual Keepass database

```cmd
pykeypass open <new_entry>
```

### Show list of configured databases

```cmd
pykeypass open
```

### Show path of individual configured database

```cmd
pykeypass open <new_entry> -p
```

## Testing

- Uses pytest and Click CliRunner
- Coverage: 94% (as of 3/8/2020)

Run simple test from root of app directory

```cmd
pytest -v test.py
```

Run Coverage

```cmd
coverage run -m pytest -v test.py
```

Generage HTML Coverage report

```cmd
coverage html
```
