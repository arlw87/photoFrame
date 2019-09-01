#sorting test
import os
import glob

def sortFilesDateMod(dir):
    #print(dir)
    files = glob.glob("%s/*.jpg"%dir)
    files.sort(reverse = True, key=os.path.getmtime)
    #print(files)
    return files
