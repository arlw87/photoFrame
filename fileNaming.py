#this file contains a function that names files for the photoFrame project
import os
import glob


def getName(dirlist):
    files = glob.glob("%s/*.jpg"%dirlist)
    highestNumber = 0
    print(dirlist)
    if len(files) == 0:
        newFileName = "0.jpg"
    else:
        for file in files:
            currentFileName = os.path.basename(file)
            try:
                stop = currentFileName.index(".")
                fileNumber = int(currentFileName[:stop])
            except:
                #if the file doesnt conform to expected structure
                #set the number to 0 so the file is ignored
                #would be good to log this!!
                fileNumber = 0
            if fileNumber > highestNumber:
                highestNumber = fileNumber
        newFileNumber = highestNumber + 1
        newFileName = "%s.jpg"%newFileNumber
    return newFileName

#for testing getName()
#dir_path = os.path.dirname(os.path.realpath(__file__))
#photoLocation = "Photos"
#path = "%s/%s" % (dir_path, photoLocation)
#print("New File Name: ", getName(path))
