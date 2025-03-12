#!/usr/bin/env python

"""my_shell.py:
simple shell that interacts with the filesystem and runs external commands.

try to stick to style guide for python code and docstring conventions:
see https://peps.python.org/pep-0008 and https://peps.python.org/pep-0257/

(note: the breakdown into input/action/output in this script is just a suggestion.)
"""

import glob
import os
import pwd
import shutil
import sys
import time

# define the directories to search for executable files
THE_PATH = ["/bin/", "/usr/bin/", "/usr/local/bin/", "./"]

# ========================
#    files command
#    list file and directory names
#    no command arguments
# ========================
def files_cmd(fields):
    """return nothing after printing names/types of files/dirs in working directory.
    
    input: takes a list of text fields
    action: prints for each file/dir in current working directory their type and name
            (unless list is non-empty in which case an error message is printed)
    output: returns no return value
    """
    
    if checkArgs(fields, 0):  # check if there are no arguments provided
        # list all files and directories in the current working directory
        for filename in os.listdir('.'):
            if os.path.isdir(os.path.abspath(filename)):  # check if it's a directory
                print("dir:", filename)
            else:
                print("file:", filename)

# ========================
#  info command
#     list file information
#     1 command argument: file name
# ========================
def info_cmd(fields):
    """list information about a file or directory"""
    
    if not checkArgs(fields, 1):  # check if there's exactly one argument
        return

    file_path = fields[1]

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return

    try:
        stat_info = os.stat(file_path)
        file_type = "directory" if os.path.isdir(file_path) else "file"
        
        # get the owner name using pwd.getpwuid
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        last_edited = time.ctime(stat_info.st_mtime)
        file_size = stat_info.st_size if not os.path.isdir(file_path) else "N/A"

        # Check if the file is executable
        executable = os.access(file_path, os.X_OK)

        print(f"File Name: {file_path}")
        print(f"Type: {file_type}")
        print(f"Owner: {owner}")
        print(f"Last Edited: {last_edited}")
        if file_type == "file":
            print(f"Size (bytes): {file_size}")
            print(f"Executable?: {executable}")
    except Exception as e:
        print(f"Error getting info: {e}")

# ----------------------
# Other functions
# ----------------------

def checkArgs(fields, num):
    """returns if len(fields)-1 == num and print an error in shell if not.
    
    input: takes a list of text fields and how many non-command fields are expected
    action: prints error to shell if the number of fields is unexpected
    output: returns boolean value to indicate if it was expected number of fields
    """

    numArgs = len(fields) - 1  # calculate the number of arguments excluding the command name
    if numArgs == num:  # check if the correct number of arguments is provided
        return True
    if numArgs > num:  # if more arguments are provided than expected
        print("Unexpected argument", fields[num+1], "for command", fields[0])
    else:  # if fewer arguments are provided than expected
        print("Missing argument for command", fields[0])
        
    return False

# ========================
#  Run external command
# ========================
def run_external_command(fields):
    """runs an external command using os.fork() and os.execv()
    
    input: takes a list of fields, with the first field being the command and subsequent ones as arguments
    action: forks a child process to run the external command using os.execv() and waits for it to complete
    output: prints the return code or an error message
    """
    
    cmd = fields[0]  # the command to be run
    execname = find_executable(cmd)

    if execname is None:
        print(f"Error: Command '{cmd}' not found in path.")
        return

    pid = os.fork()  # create a child process
    if pid == 0:  # child process
        try:
            os.execv(execname, fields)  # replace the child process with the external command
        except Exception as e:
            print(f"Error executing command: {e}")
            os._exit(1)  # exit the child process with error code 1
    else:  # parent process
        pid, status = os.waitpid(pid, 0)  # wait for the child process to complete
        if os.WIFEXITED(status):
            print(f"Command '{cmd}' executed successfully with return code {os.WEXITSTATUS(status)}.")
        else:
            print(f"Command '{cmd}' exited abnormally.")

# ========================
#  Find executable in PATH
# ========================
def find_executable(cmd):
    """searches for the command in the directories listed in THE_PATH.
    
    input: the command name
    action: checks each directory in THE_PATH to see if the command is an executable file
    output: returns the full path of the executable file if found, or None if not found
    """
    
    if cmd[0] not in ['/', '.']:  # if the command is a relative or absolute path
        for dir in THE_PATH:
            execname = os.path.join(dir, cmd)
            if os.path.isfile(execname) and os.access(execname, os.X_OK):
                return execname
        return None
    else:
        return cmd

# ---------------------------------------------------------------------

def main():
    """returns exit code 0 (after executing the main part of this script).
    
    input: no function arguments
    action: run multiple user-inputted commands
    output: return zero to indicate regular termination
    """
    
    while True:
        line = input("PShell>")
        fields = line.split()  # split the command into fields stored in the fields list
        # fields[0] is the command name and anything that follows (if it follows) is an argument to the command
        
        if fields[0] == "files":
            files_cmd(fields)
        elif fields[0] == "info":
            info_cmd(fields)
        elif fields[0] == "exit":
            print("Exiting shell...")
            sys.exit(0)
        else:
            run_external_command(fields)  # run external commands
        
    return 0  # currently unreachable code

if __name__ == '__main__':
    sys.exit(main())  # run main function and then exit

