#main file
from gDrive import GDrive
from Email import Gmail
import time
import os
import logging
import timeCheck as timeFunctions
from settings import Settings
from weeklyReport import WeeklyReport


#move the mouse on start up
moveMouse = "xdotool mousemove 500 500"
os.system(moveMouse)

#settings
frameSettings = Settings()
ImagesRxReportLocation = frameSettings.ImagesReceivedReportPath

fn = "%s/appDebug.log"%ImagesRxReportLocation
#set up the debugger log
logging.basicConfig(filename=fn, format='%(name)s - %(levelname)s - %(message)s')
#test logger
logging.debug('This will get logged')

#settings for program
dir_path = os.path.dirname(os.path.realpath(__file__))
creditFileName = "mycredits.txt"
creditsLocation = "%s/%s"%(dir_path, creditFileName)
listName = "downLoadList.json"
listLocation = "%s/%s"%(dir_path, listName)
photoLocation = "Photos"
gDriveQuery = "'root' in parents and trashed=false"

#Setup gDrive
#From the setting file
photoFrameEmail = frameSettings.photoFrameEmail
pswd = frameSettings.pswd
server = frameSettings.email_server
port = frameSettings.email_port
reportEmail = frameSettings.report_email

gDrive = GDrive(creditsLocation, listLocation, ImagesRxReportLocation)

#setup Email
email = Gmail(photoLocation, ImagesRxReportLocation, photoFrameEmail, pswd, server, port)

#create weeklyReport object
#for testing
rxEmail = ""
txEmail = ""
ReportLocation = ImagesRxReportLocation
CounterLocation = frameSettings.CounterLocation
DaysBetweenReports = frameSettings.DaysBetweenReports

wr = WeeklyReport(ReportLocation, CounterLocation, DaysBetweenReports)

while True:
    #this below if statement will be used in production
    #check for files every hour
    time.sleep(10)
    if timeFunctions.checkTimeImage(True, frameSettings.ImagesminutesToCheck):
        print("Checking For Images")
        #Gdrive Code
        #inside a try block. If at any point during checking gDrive
        #the internet drops out an error will occur. This will be captured in the
        #log file and the code will move on, and another try will occur later
        #It is possible this will put the connection into a unknown state that
        #could make any future attempts to log in problematic
        try:
            gDrive.Authorize()
            gDrive.Connect()
            gDrive.LoadDownLoadList()
            gDrive.DownloadNewImages(photoLocation, gDriveQuery)
        except Exception as ex:
            logging.exception('Error in the gDrive Code')
            print("Error Written to App.log")
        #Email Code
        #inside a try block. If at any point during checking the emails
        #the internet drops out an error will occur. This will be captured in the
        #log file and the code will move on, and another try will occur later
        #It is possible this will put the connection into a unknown state that
        #could make any future attempts to log in problematic
        try:
            email.connectServer()
            email.login()
            email.getEmail('Photos')
            email.downLoadImages()
            #check for emails with key word Photo
            email.getEmail('Photo')
            email.downLoadImages()
            email.logout()
        except Exception as ex:
            logging.exception('Error in the Receive Email Code')
            print("Error Written to App.log")

        #for testing this will be keep at 50 seconds
        #in production this will be 60 seconds
        time.sleep(65)

    else:

        print("Not Checking At the Moment")

    #Sending weekly report
    #for production
    if timeFunctions.checkTimeReport(frameSettings.reportMinutesToCheck, frameSettings.reportHoursToCheck):
    #report is sent regularly, the timeToSendReport method will determine whether to send then
    #report and if not will iterate the saved counter
        print("In Report Send Section")
        if wr.timeToSendReport():
            print("Time to send the email")
            emailSubject = frameSettings.emailSubject
            emailMessage = frameSettings.emailMessage
            try:
                wr.sendReport(photoFrameEmail, reportEmail, emailSubject, pswd, emailMessage)
            except Exception as ax:
                logging.exception('Error in the send Email Code')
                print("Error Written to App.log")
            #only want to do this once a day
            time.sleep(65)
        else:
            print("Dont time to send email")
            #if not time to send report one want one iteration
            time.sleep(65)
        time.sleep(0)
