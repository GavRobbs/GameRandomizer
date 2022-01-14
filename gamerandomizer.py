import os
import random
import sys, getopt

def getDesiredROMCount():
    #Asks the user how many roms they want to select from, loops until it gets a valid input
    asking = True
    numFiles = 0

    while asking:
        try:
            numFiles = int(input("Please enter the number of games you'd like randomly selected for analysis: "))
            asking = False
        except ValueError:
            print("Invalid input, please try again")
    
    return numFiles


def getAllFilesInRomDirectory(romDirectory):
    #Lists all files in the working directory

    all_files = os.listdir(romDirectory)

    if(len(all_files) == 1):
        print("Please put this script in the directory containing your rom files")
        return []
    else:
        return all_files

def pickROMS(rom_list, count):
    #This function does the randomization from the list of roms obtained
    selections = []
    i = 0

    #Ensures that we don't ask for more ROM files than are available in the folder
    lower = min(len(rom_list), count)

    while i in range(0, lower):
        selections.append(random.choice(rom_list))
        i += 1
    
    return selections

def main(dir, romFormats):
    print("Welcome to the Game Randomizer.")
    print("You can use this small program to pick a specified number of random ROMS from a folder containing a collection of them.")

    numFiles = getDesiredROMCount()
    all_files = getAllFilesInRomDirectory(dir)

    #Filters the rom files from all the files in the directory
    rom_files = list(filter(lambda f: f[-3:] in romFormats, all_files))

    if(len(rom_files) == 0):
            print("No valid ROM files found")
            return

    #The main loop of the program - picks roms until the user no longer wants to do that
    picking = True
    while picking:

        selected_files = pickROMS(rom_files, numFiles)    

        print("\nThe games that have been chosen for you are: ")
        for count, fileName in enumerate(selected_files):
            print(str(count + 1) + ": " + fileName)


        pickAgain = str(input("\nDo you want to pick again(Y/N)? ")).upper()
        if pickAgain == 'Y':
            picking = True
        else:
            print("Thank you! Goodbye!")
            picking = False

if __name__ == '__main__':
    directory = os.getcwd()
    romformats = ["zip"]
    
    #Parse the command line arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "hd:f:", ["help", "directory=", "romformat="])

        for opt, arg in options:
            if opt in ('-h', "--help"):
                print("gamerandomizer.py -d <path to search directory> -f <rom file format>")
                print("The default rom file formats that are searched for are zip and smc, but to specify any custom formats, enter them as comma separated values with no spaces eg. 'zip,smc'")
                sys.exit()
            elif opt in ("-d", "--directory"):
                directory = arg
            elif opt in ("-f", "--romformat"):
                romformat = arg.split(',')
            else:
                raise getopt.GetoptError
    except (getopt.GetoptError, ValueError):
        #If there is an error parsing the arguments, display the error message and quit
        print("You have entered invalid command line arguments. Type 'gamerandomizer.py -h' or 'gamerandomizer.py --help' for usage instructions")
        sys.exit()

    main(directory, romformats)
