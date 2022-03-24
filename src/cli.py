# Import modules
import os
import sys
from modules.vault_manager import *
from hashlib import md5

# Utility
def getMD5(plaintext):
    m = md5()
    m.update(plaintext.encode('utf-8'))
    hash = str(m.hexdigest())
    return hash

# Authentication
if os.path.isfile('auth'):
    savedpassword = open('auth', 'r').read()
    password = str(input("Enter password: "))
    pwdhash = getMD5(password)
    if pwdhash == savedpassword:
        pass
    else:
        sys.exit("Wrong password")
else:
    password = str(input("Enter new password: "))
    pwdhash = getMD5(password)
    open('auth', 'w').write(pwdhash)


# Constants
fileMan = fileManager(password)
uploadDir = 'modules/DATA/files/upload/'
tmpPath = 'modules/DATA/files/tmp/'
# Loop for continuous commands
command = None
while command != 0:
    # List options
    command = int(input("1) Add file 2) Delete file 3) List files 4) Clear data 5) Open file 0) Exit "))
    # Run options
    if command == 0:
        print("Saving edits")
        for filename in os.listdir(tmpPath):
            fileMan.rm(filename)
            uploadPath = str(uploadDir + filename)
            filepath = str(tmpPath + filename)
            shutil.copy(filepath, uploadPath)
            fileMan.add(filename)
        print("Clearing tmp and Exiting...")
        shutil.rmtree('modules/DATA/files/tmp')
        os.mkdir('modules/DATA/files/tmp')
        sys.exit(0)
    elif command == 1:
        filepath = str(input("Enter path to file: "))
        try:
            filename = os.path.basename(filepath)
            uploadPath = str(uploadDir + filename)
            shutil.copy(filepath, uploadPath)
            fileMan.add(filename)
        except Exception as e:
            print(e)
        print("File added")
    elif command == 2:
        try:
            fileMan.rm(str(input("Enter filename: ")))
        except Exception as e:
            print(e)
    elif command == 3:
        try:
            for file in fileMan.ls('/'):
                print(file)
        except Exception as e:
            print(e)
    elif command == 4:
        try:
            fileMan.clear()
            os.remove('auth')
            sys.exit('All data cleared.')
        except Exception as e:
            print(e)
    elif command == 5:
        fileMan.open(str(input("Enter filename")))
    else:
        print("Not a command")
