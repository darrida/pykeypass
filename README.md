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
  - [Notes about development history](#notes-about-development-history)

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
- Linux (*untested*)
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

- Input password when directed.
- If the setup completes successfully, the following will appear:

```cmd
DONE: pykeypass app database created.
Setup keepass databases by using:
- 'pykeypass open <new_name> -s'
```

- **NOTE:** If a pykeypass app database already exists an additional prompt will appear with a warning that proceeding will delete the current database and create a new one.

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

## Notes about development history

- [ ] Clean up copy here

- **VBScript:** The very first version of this was built in VBScript in 2014 (and yes, VBS was old then as well): <https://github.com/darrida/KeePass_Login_App>
  - I actually used the VBS version up until just a few months ago. I had built a number of Python based CLI apps at that point, but because the VBS thing worked "ok" *enough* it took me a long time to get around to rewriting it.
  - In this version everything was hardcoded. I hardcoded entries in my config ini file so that I could have one Keepass database that required the use of a password *and* a security key file, and two Keepass databases that only required a password.
  - This version also tried to depend on a combination of obsurity and access to multiple locations for security.
    - The ini file with the hashed passwords was stored on an encypted USB drive that was plugged in and decrypted every morning.
    - The main portion of the VBS script was stored locally
    - The VBS decrypte file was stored separately in a network storage location associated with my active directory login.
  - Needless to say, this was probably more complicated than it was worth, BUT I really enjoyed the challenge and satifaction of writing it. It also meant that I was able to enjoy that satisfaction everyday when I launched the Keepass databases my work depended on.
  - One of the major draw backs of this version is that I never updated it to take advantage of the Keepass command line support. The VBS script was literally launching the Keepass application, launching the open file dialogue, and tabbing and pasting strings into the interface. This was easily disrupted by other items loading during the initial login sequence.
- **Python:** More recently, after using Python to varying degress for a good 3 years or so, I finally got around to rewriting the tool.
  - The first iteration pretty much copied the hardcoded nature of the VBS version, but it took advantage of the Keepass command line support.
    - The big improvement was that all of launch/login activity took place before the fully logged in Keepass window appeared. It also was no longer interrupted by other loading processes.
    - This version incorperated no flexibility, as it was coded specifically for the specific Keepass files that I depended on.
    - At this point there were three functions, one for each of the two Keepass files I use, and one that facilitate launching both files at ones.
  - The second iteration was to incorperate more flexibility into one of the two files that I launch.
    - Why not both files? Well, that's primarily because there is one common file that used by many people, which never changes. The information related to that file I left hardcoded. This file also requires a security key file, which just takes a little more work to manage.
    - This version also included a rudementary wizard for configuring the one flexible file.
  - The third iteration involved moving away from storing hashed (but reversible) passwords in a flat file.
    - I found pykeepass, a Python package that makes working with Keepass databases easy (<https://github.com/libkeepass/pykeepass).>
    - I used pykeepass to utilitize a Keepass database for the storage and retrieval of information I used to launch and login to the Keepass databases I depend on. A major benefit of this is depending on Keepass's own secure storage for storing sensitive information.
  - The fourth interation was another major rewrite that allowed the creation of virtually unlimited Keepass database entries (both with and without security file keys).
    - Removed all hardcoded elements
    - Moved storage of configuration information to a ".pykeypass" folder in the home directory
    - Rewrote all install, uninstall, and Keepass entry setup processes to make it more straightforward and handle errors much more effectively (including a large number of responses that help the user setup things up correctly).
    - Requires much less understanding of the tool in order to use it.
  
