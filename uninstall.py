# Local
import os
import shutil
from pathlib import Path

########## GLOBAL VARIABLES ###########
pykeypass_folder = Path.home() / ".pykeypass"
pykeypass_app = pykeypass_folder / "keepass.exe"
pykeypass_db = pykeypass_folder / "pykeepass.kdbx"
#######################################


def pykeypass_remove():
    try:
        print("START: Checking for existence of pykeypass directory")
        if os.path.exists(pykeypass_folder) is True:
            confirm = input(
                "CONFIRM: This will remove the pykeypass app database from the home directory. "
                "Continue? (y/n) "
            )
            if confirm == "y":
                print("PROGRESS: pykeypass directory located. Removing...")
                shutil.rmtree(pykeypass_folder)
                # if result == None:
                if os.path.exists(pykeypass_folder) is False:
                    print(
                        "DONE: Files associated with pykeypass have been removed from home "
                        "directory."
                    )
                else:
                    print(
                        'ERROR: Unable to remove pykeypass directory. To remove manually, delete '
                        '"pykeypass_app_files" in the user home directory.'
                    )
            else:
                print("DONE: Removal of pykeypass app database cancelled.")
        else:
            print("DONE: No action -- pykeypass directory not found in home directory.")
    except PermissionError:
        print(
            "ERROR: Uninstall.py was denied permission to modify the pykeypass app database. If "
            "the database is open, please close and try again."
        )


if __name__ == "__main__":
    pykeypass_remove()
