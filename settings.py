# settings file for Nanny Photo frame
import os

class Settings():
    """class to hold all the settings for the photoFrame"""
    def __init__(self):

        #window dimenstions
        self.width = 1920
        self.height = 1200

        #location of root where the python files are located
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.photo_path = '/Photos'

        #interval between photos
        self.minutes = 10
        self.time = int(self.minutes * 60000)
        #the duration before images saved are not considered recent and
        #go into the random list and are not the first up
        # in seconds
        # for testing made an hour
        # Two Days
        self.recent = 172800

        #setting for when to check for new files

        #once a day check to see if you need to send the weekly report
        self.reportHoursToCheck = 12
        self.reportMinutesToCheck = 22

        #this is a list to allow for multiple checks an hour
        self.ImagesminutesToCheck = [0]

        #for i in range(0, 60, 1):
        #    self.ImagesminutesToCheck.append(i)

        #Images Received Report
        #There will only be one file that will grow over time and be
        #regularly Sent
        self.ImagesReceivedReportPath = "%s/ImageReport.log"%self.dir_path

        self.CounterLocation = "%s/Counter.log"%self.dir_path

        #how often to send email reports to developer
        #self.DaysBetweenReports = 7
        self.DaysBetweenReports = 7 #testing this is every hour

        #email Settings
        #update with own settings
        self.photoFrameEmail = ""
        self.pswd = ""
        self.email_server = "imap.gmail.com"
        self.email_port = 993
        self.report_email = ""

        #report settings
        self.emailSubject = "Weekly PhotoFrame Report"
        self.emailMessage = "Please see the attachment"

        #ammount of phtotos in new random Section
        self.oldRandomPhotos = 30
        self.newRandomPhotos = 30
