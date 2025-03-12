#!/usr/bin/env python

from datetime import datetime
import os
import shutil
import sys
import pwd  # to get user name instead of uid

THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]

# ========================
#   run command
# ========================
def runCmd(fields):
    global THE_PATH
    cmd = fields[0]
    execname = add_path(cmd, THE_PATH)  # find the executable file in specified paths

    if execname == None:
        print("Executable file", cmd, "not found")
    else:
        print(execname)
        try:
            # execute the file with provided arguments
            os.execv(execname, fields)
        except:
            # handle execution errors
            print("Something went wrong there")
            os._exit(0)

# function to check if an executable exists in the given directories
def add_path(cmd, executable_dirs):
    if cmd[0] not in ['/', '.']:  # check if cmd is not an absolute or relative path
        for dir in executable_dirs:
            execname = dir + cmd  # check each directory for the executable file
            if os.path.isfile(execname) and os.access(execname, os.X_OK):  # verify it's executable
                return execname
        return None
    else:
        return cmd

# ========================
#  files command
# ========================
def filesCmd(fields):
    """list files and directories in the current directory"""
    try:
        # list all files and directories in the current working directory
        for filename in os.listdir(os.getcwd()):
            if os.path.isdir(filename):
                print(f"{filename}/")  # indicate it's a directory
            else:
                print(filename)  # print the file name
    except Exception as e:
        print(f"Error listing files: {e}")

# ========================
#  info command
# ========================
def infoCmd(fields):
    """list information about a file or directory"""
    if not checkArgs(fields, 1):  # ensure one argument is provided (the file or directory)
        return

    file_path = fields[1]

    if not os.path.exists(file_path):  # check if the file or directory exists
        print(f"Error: {file_path} does not exist.")
        return

    try:
        # retrieve file status using os.stat
        stat_info = os.stat(file_path)
        file_type = "directory" if os.path.isdir(file_path) else "file"  # determine file type
        
        # get the owner name using pwd.getpwuid
        # https://stackoverflow.com/questions/1830618/how-to-find-the-owner-of-a-file-or-directory-in-python
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        last_edited = datetime.fromtimestamp(stat_info.st_mtime).strftime('%a %b %d %H:%M:%S %Y')
        file_size = stat_info.st_size if not os.path.isdir(file_path) else "N/A"

        # check if the file is executable
        executable = os.access(os.path.abspath(file_path), os.X_OK)

        # print information about the file
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
    """delete a specified file"""
    if not checkArgs(fields, 1):  # ensure one argument is provided (the file to delete)
        return

    file_path = fields[1]

    if not os.path.exists(file_path):  # check if the file exists
        print(f"Error: {file_path} does not exist.")
        return

    try:
        # remove the file using os.remove
        os.remove(file_path)
        print(f"Successfully deleted {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

# ========================
#  copy command
# ========================
def copyCmd(fields):
    """copy a file to a new name"""
    if not checkArgs(fields, 2):  # ensure two arguments are provided (source and destination)
        return

    source = fields[1]
    destination = fields[2]

    if not os.path.exists(source):  # check if the source file exists
        print(f"Error: {source} does not exist.")
        return

    if os.path.exists(destination):  # check if the destination file already exists
        print(f"Error: {destination} already exists.")
        return

    try:
        # copy the file from source to destination using shutil.copy
        shutil.copy(source, destination)
        print(f"Successfully copied {source} to {destination}")
    except Exception as e:
        print(f"Error copying file: {e}")

# ========================
#  make command
# ========================
def makeCmd(fields):
    """create a new empty file"""
    if not checkArgs(fields, 1):  # ensure one argument is provided (the filename)
        return

    filename = fields[1]

    if os.path.exists(filename):  # check if the file already exists
        print(f"Error: {filename} already exists.")
        return

    try:
        # create an empty file by opening it in write mode
        with open(filename, 'w') as f:
            pass
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error creating file: {e}")

# ========================
#  down command
# ========================
def downCmd(fields):
    """change to a specified directory"""
    if not checkArgs(fields, 1):  # ensure one argument is provided (the directory name)
        return

    dir_name = fields[1]

    if not os.path.isdir(dir_name):  # check if the directory exists
        print(f"Error: {dir_name} does not exist.")
        return

    try:
        # change to the specified directory using os.chdir
        os.chdir(dir_name)
        print(f"Changed to directory {dir_name}")
    except Exception as e:
        print(f"Error changing directory: {e}")

# ========================
#  up command
# ========================
def upCmd(fields):
    """change to the parent directory"""
    try:
        # change to the parent directory using os.chdir("..")
        os.chdir("..")
        print("Changed to parent directory")
    except Exception as e:
        print(f"Error changing to parent directory: {e}")

# ========================
#  finish command
# ========================
def finishCmd(fields):
    """exit the shell"""
    print("Exiting shell...")
    sys.exit(0)

# ========================
#  checkArgs function
# ========================
def checkArgs(fields, num):
    """check if the number of arguments is correct"""
    numArgs = len(fields) - 1
    if numArgs == num:  # check if the correct number of arguments is provided
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
        fields = line.split()  # split the input into fields (command and arguments)
    
        # handle different commands
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

