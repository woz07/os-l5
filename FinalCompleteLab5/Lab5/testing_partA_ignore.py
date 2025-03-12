#!/usr/bin/env python

from datetime import datetime
import os
import shutil
import sys
import pwd # to get user name instead of uid

THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]

# ========================
#   Run command
# ========================
def runCmd(fields):
    global THE_PATH
    cmd = fields[0]
    execname = add_path(cmd, THE_PATH)

    if execname == None:
        print("Executable file", cmd, "not found")
    else:
        print(execname)
        try:
            os.execv(execname, fields)
        except:
            print("Something went wrong there")
            os._exit(0)

def add_path(cmd, executable_dirs):
    if cmd[0] not in ['/', '.']:
        for dir in executable_dirs:
            execname = dir + cmd
            if os.path.isfile(execname) and os.access(execname, os.X_OK):
                return execname
        return None
    else:
        return cmd

# ========================
#  files command
# ========================
def filesCmd(fields):
    """List files and directories in the current directory"""
    try:
        for filename in os.listdir(os.getcwd()):
            if os.path.isdir(filename):
                print(f"{filename}/")
            else:
                print(filename)
    except Exception as e:
        print(f"Error listing files: {e}")

# ========================
#  info command
# ========================
def infoCmd(fields):
    """List information about a file or directory"""
    if not checkArgs(fields, 1):
        return

    file_path = fields[1]

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    try:
        stat_info = os.stat(file_path)
        file_type = "directory" if os.path.isdir(file_path) else "file"
        
        # Get the owner name using pwd.getpwuid
        # https://stackoverflow.com/questions/1830618/how-to-find-the-owner-of-a-file-or-directory-in-python
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        last_edited = datetime.fromtimestamp(stat_info.st_mtime).strftime('%a %b %d %H:%M:%S %Y')
        file_size = stat_info.st_size if not os.path.isdir(file_path) else "N/A"

        # Check if the file is executable
        # Having issues here, won't work properly, skipped for now
        # Could just make an array of known executable's and check against that with split
        # but that could be unreliable as new executable's get released
        executable = os.access(os.path.abspath(file_path), os.X_OK)

        print(f"File Name: {file_path}")
        print(f"Directory/File: {file_type}")
        print(f"Owner: {owner}")
        print(f"Last Edited: {last_edited}")
        if file_type == "file":
            print(f"Size (bytes): {file_size}")
            print(f"Executable?: {executable}")
    except Exception as e:
        print(f"Error getting info: {e}")


# ========================
#  delete command
# ========================
def deleteCmd(fields):
    """Delete a specified file"""
    if not checkArgs(fields, 1):
        return

    file_path = fields[1]

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    try:
        os.remove(file_path)
        print(f"Successfully deleted {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

# ========================
#  copy command
# ========================
def copyCmd(fields):
    """Copy a file to a new name"""
    if not checkArgs(fields, 2):
        return

    source = fields[1]
    destination = fields[2]

    if not os.path.exists(source):
        print(f"Error: {source} does not exist.")
        return

    if os.path.exists(destination):
        print(f"Error: {destination} already exists.")
        return

    try:
        shutil.copy(source, destination)
        print(f"Successfully copied {source} to {destination}")
    except Exception as e:
        print(f"Error copying file: {e}")

# ========================
#  make command
# ========================
def makeCmd(fields):
    """Create a new empty file"""
    if not checkArgs(fields, 1):
        return

    filename = fields[1]

    if os.path.exists(filename):
        print(f"Error: {filename} already exists.")
        return

    try:
        with open(filename, 'w') as f:
            pass
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error creating file: {e}")

# ========================
#  down command
# ========================
def downCmd(fields):
    """Change to a specified directory"""
    if not checkArgs(fields, 1):
        return

    dir_name = fields[1]

    if not os.path.isdir(dir_name):
        print(f"Error: {dir_name} does not exist.")
        return

    try:
        os.chdir(dir_name)
        print(f"Changed to directory {dir_name}")
    except Exception as e:
        print(f"Error changing directory: {e}")

# ========================
#  up command
# ========================
def upCmd(fields):
    """Change to the parent directory"""
    try:
        os.chdir("..")
        print("Changed to parent directory")
    except Exception as e:
        print(f"Error changing to parent directory: {e}")

# ========================
#  finish command
# ========================
def finishCmd(fields):
    """Exit the shell"""
    print("Exiting shell...")
    sys.exit(0)

# ========================
#  checkArgs function
# ========================
def checkArgs(fields, num):
    """Check if the number of arguments is correct"""
    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:
        print("Missing argument for command", fields[0])
    
    return False

# ========================
#  main function
# ========================
def main():
    while True:
        line = input("PShell>")
        fields = line.split()
    
        if fields[0] == "files":
            filesCmd(fields)
        elif fields[0] == "info":
            infoCmd(fields)
        elif fields[0] == "delete":
            deleteCmd(fields)
        elif fields[0] == "copy":
            copyCmd(fields)
        elif fields[0] == "make":
            makeCmd(fields)
        elif fields[0] == "down":
            downCmd(fields)
        elif fields[0] == "up":
            upCmd(fields)
        elif fields[0] == "finish":
            finishCmd(fields)
        else:
            runCmd(fields)

    return 0

if __name__ == '__main__':
    sys.exit(main())

