#Class for getting photos from gDrive

#import some libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import json
import fileNaming
import reportCreate as report


class GDrive():
    def __init__(self, creditsLocation, ListLocation, logFilePath):
        self.fileNumber = 0
        self.downLoadList = []
        self.gauth = GoogleAuth()
        self.CreditsLocation = creditsLocation
        self.ListLocation = ListLocation
        self.logFilePath = logFilePath


    def Authorize(self):
        self.gauth.LoadCredentialsFile(self.CreditsLocation)
        if self.gauth.credentials is None:
            #Authenticate through browser if it hasnt been done yet
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialise the saved credentials
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile(self.CreditsLocation)

    def Connect(self):
        self.drive = GoogleDrive(self.gauth)

    def LoadDownLoadList(self):
        #this function will load a json file which will have the fileID and
        #local file name so that duplicates are not downloaded
        try:
            with open(self.ListLocation, 'r') as fo:
                self.downLoadList = json.load(fo)
            print(self.downLoadList)
        except:
            print("No File")

    def SaveLatestDownLoadList(self):
        try:
            with open(self.ListLocation, 'w') as fo:
                 json.dump(self.downLoadList, fo)
            print("Download List File Saved")
        except:
            print("Download List File Not Saved")


    def DownloadNewImages(self, PhotoLocation, strQuery):
        file_list = self.drive.ListFile({'q': strQuery}).GetList()

        for file in file_list:
            #for debugging
            print('-' * 20)
            #print(file)
            #print(file["mimeType"])
            print('-' * 20)

            #if the file type is not an image then dont download
            if file["mimeType"] != "image/jpeg":
                print("Not an image")
                continue

            #get working directory
            dir_path = os.path.dirname(os.path.realpath(__file__))
            #get photos directory
            directory_path = "%s/%s"%(dir_path, PhotoLocation)
            #if the file from gDrive has not been downloaded already
            if file['id'] not in self.downLoadList:
                fileName = fileNaming.getName(directory_path)
                filePath = "%s/%s/%s"%(dir_path, PhotoLocation, fileName)
                print("New File!")
                print(filePath)
                #get file
                photo = self.drive.CreateFile({'id': file['id']})
                #download file
                photo.GetContentFile(filePath)
                #add to the download list
                self.downLoadList.append(file['id'])
                #log that this new file has been saved
                self.logDownload(file)

            else:
                print("%s has already been Downloaded" %file['id'])

            self.SaveLatestDownLoadList()
            #at the end of each iteration i want to save the DownLoad List
            #This is because if the program stops mid iteration of the file
            #list and there is a lot of new files these would be redownload


    def logDownload(self, file):
        #lets get some useful info to save
        try:
            fileUniqueID = file['id']
        except:
            fileUniqueID = "Cant Get ID"
        try:
            fileName = file['originalFilename']
        except:
            fileName = "Cant get Filename"
        try:
            modifiedDate = file['modifiedDate']
        except:
            modifiedDate = "Cant get modified Date"

        logIntro = "A new file has been downloaded from GDrive, here is its information"

        #create the info list
        Info = [fileUniqueID, fileName, "Uploaded Date: ", modifiedDate]

        report.logToFile(self.logFilePath, logIntro, Info)
