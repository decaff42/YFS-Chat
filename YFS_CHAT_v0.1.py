"""YFS Chat Extract
Run this script with a YFS file in the same directory.

Tested with Python 3.4.2. Your milage may varry with other versions of Python.
"""

import os

__title__       = "YFS Chat Extract"
__author__      = "Decaff_42"
__version__     = "0.1"


def Print_Title():
    """Prints the introductory title"""
    print(__title__)
    print("By: "+__author__)
    print("Version "+__version__+"\n")

def main():
    """Run through all YFS files in directory and create a text file
    with the chat log."""

    # Print the Shell window header
    Print_Title()

    # Prepare Parameters
    cwd         = os.getcwd()
    yfs_files   = []
    txt_files   = []

    # Get list of YFS and text files
    for file in os.listdir(cwd):
        if file.endswith(".yfs"):
            yfs_files.append(file)
        elif file.endswith(".txt"):
            txt_files.append(file)

    # Ignore files that have already been parsed
    for txt in txt_files:
        n = txt[:-4] + ".yfs"
        if n in yfs_files:
            print("Found [{}] and ignoring".format(n))
            del yfs_files[yfs_files.index(n)]

    # If no YFS files, cry!
    if len(yfs_files) == 0:
        print("\nYou Done Goofed Mate!")
        print(("{} has not found any YFS Files in this directory to parse."
               "\nIf there are files, they may have already been parsed."
               "".format(__title__)))
        raise Exception("Error: No .yfs files to parse in directory!")
    

    # Parse each YFS file in the directory.
    for filename in yfs_files:
        Parse(filename)

def Before(time):
    """Figures out the time before the decimal point"""
    return len(time.split(".")[0])

def Parse(filename):
    """Parse the YFS file to get the text event data
    Start recording data at: EVTBLOCK
    Stop recording data at: EDEVTBLK"""

    # Import file as a list of strings
    with open(filename,newline=None) as file:
        yfs_data = file.read().splitlines()

    print("Imported {}".format(filename))
    # Read through until finding the start of the event block
    Active = False
    row = 0
    while Active is False:
        if "EVTBLOCK" in yfs_data[row]:
            Active = True
        else:
            row += 1

    # Get all chat events
    output = [] # Output should have "[TIME] - TEXT MESSAGE" format
    max_before = 0
    while Active is True:
        if "TXTEVT" in yfs_data[row]:
            time = yfs_data[row].split(" ")[1]
            msg = yfs_data[row+1][4:]
            if max_before > Before(time):
                max_before = Before(time)
            output.append([Before(time),time,msg])
            row += 3
        elif "EDEVTBLK" in yfs_data[row]:
            Active = False
            row+=1
        else:
            row+=1

    # Format Time values
    writer = []
    for row in output:
        b       = row[0]
        time    = row[1]
        msg     = row[2]
        
        # Add leading zeros before time if needed
        if b < max_before:
            time = (max_before-b)*"0"+time

        # Trim trailing time values after second decimal places
        time = time.split(".")[0]+"."+time.split(".")[-1][0:2]

        # Store data
        writer.append("{} - {}".format(time,msg))
        
    # Save file
    fname = filename[:-4]+".txt"
    
    with open(fname,"w") as file:
        file.write("\n".join(writer))

    print("Saved {} chat messages to {}\n".format(len(output),fname))

    
# Run the code!
main()
    
    
