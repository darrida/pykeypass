# pykeypass

pykeypass (because pykeepass was already taken) uses the pykeepass library to manage and launch multiple Keepass libraries

**Table of Contents**

- [pykeypass](#pykeypass)
  - [Background](#background)
  - [Setup and remove](#setup-and-remove)
    - [Setup](#setup)
    - [Remove](#remove)
  - [Usage](#usage)
    - [Setup standalone Keepass executable and app database:](#setup-standalone-keepass-executable-and-app-database)
    - [Setup a new Keypass database entry](#setup-a-new-keypass-database-entry)
    - [Open all Keepass databases](#open-all-keepass-databases)
    - [Open individual Keepass database](#open-individual-keepass-database)
    - [Show list of configured databases](#show-list-of-configured-databases)
    - [Show path of individual configured database](#show-path-of-individual-configured-database)

## Background

This is a tool that I use almost everyday, both at home and at work. 

(Well, it's actually just the latest iteration of this tool. The first of many versions was in 2014 when all I knew how to use was VBScript. Things have imporved a *bit* over the last 5-6 years)

**THE PROBLEM:**
At work I typically have 2-3 different Keepass databases open at the same time. This means that after I arrived on any given day one of the first things I would do is open Keypass. After that I would proceed to open the "File" menu, select the first item out of the recents section, and input the password. Then, again, I'd open the "File" menu and repeat the same set of steps a couple of more times. 

Occassionally I'd find that something cleared out the recents options, which means that I would have to manually browser to the different network directory locations where each Keepass database lived to open them.

**THE SOLUTION:**
pykeypass allows me to open the Command Prompt, type ```pykeypass all```, input a single password, then sit back and watch all of my Keypass databases open programmatically.

## Setup and remove

### Setup

1. Prerequisites:
   - Python 3.x must be installed (tested on Python 3.7 and 3.8)

2. Download application files
   - Option 1: Download and unzip the latest release
   - Option 2: Clone the repository

3. Install pykeypass (enable global command line availability)
   - Windows only
     - Launch **install.bat**
   - Windows or Linux (needs additional testing)
     - Open the terminal from the pykeypass directory
     - Run ```pip install -editable .```

### Remove

- Windows
  - Launch **uninstall.bat**
- Linus
  - Launch **uninstall.sh**
  - NOTE: if running from the terminal, the following may be required:
    - ```chmod u+x uninstall.sh```
    - ```./uninstall.sh```

## Usage

### Setup standalone Keepass executable and app database:

```cmd
C:\> pykeypass setup
Create a pykeypass password:
```

Input password when directed.

If the setup completes successfully, the following will appear:

```cmd
DONE: pykeypass app database created.
Setup keepass databases by using:
- 'pykeypass open <new_name> -s'
```

**NOTE:** If a pykeypass app database already exists an additional prompt will appear with a warning that proceeding will delete the current database and create a new one.

### Setup a new Keypass database entry

- Initiate the entry setup dialogue using: ```pykeypass open <new_entry> -s```
  - pykeypass will walk through the following:
    - (1) Specifying the new Keepass database url
    - (2) Specifying the password
    - (3) Whether or not the Keepass database uses a paired security key
- Standard Example:

```cmd
C:\> pykeypass open new_entry -s
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
C:\> pykeypass open new_entry -s
START: Setup database_with_key keepass.
pykeypass password:
Set database_with_key Keepass url: C:\Users\<user>\Documents\database.kdbx
Set database_with_key Keepass Password:
Does this Keepass database use a key file? (y/n) y
Set key file (file path + file name): C:\Users\<user>\Documents\database.key
DONE: database_with_key keepass password setup.
Try launching with "pykeypass open database_with_key", or "pykeypass all"
```

### Open all Keepass databases

```cmd
C:\> pykeypass all
```

### Open individual Keepass database

```cmd
C:\> pykeypass open new_entry
```

### Show list of configured databases

```cmd
C:\> pykeypass open
```

### Show path of individual configured database

```cmd
C:\> pykeypass open new_entry -p
```
