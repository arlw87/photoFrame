#Email class

#import libraries
import imaplib
import base64
import os
import email
import fileNaming
import time
import reportCreate as report

class Gmail():

    def __init__(self, PhotoLocation, logFilePath, photoFrameEmail, pswd, server, port):
        self.PhotoLocation = PhotoLocation
        self.email_Address = photoFrameEmail
        self.email_pass = pswd
        self.serverAddress = server
        self.port = port
        self.logFilePath = logFilePath


    def connectServer(self):
        self.mail = imaplib.IMAP4_SSL(self.serverAddress, self.port)

    def login(self):
        self.mail.login(self.email_Address, self.email_pass)

    def getEmail(self,enteredSubject):
        self.mail.select('Inbox')
        headerSearch = 'HEADER Subject "%s"'%enteredSubject
        self.type, self.data = self.mail.search(None, '(UNSEEN %s)'%headerSearch)
        print("Getting Emails")
        print(self.data)

    def downLoadImages(self):
        for num in self.data[0].split():
            typ, dataTemp = self.mail.fetch(num, '(RFC822)' )
            raw_email = dataTemp[0][1]
            raw_email_string = raw_email.decode('utf-8')
            self.email_message = email.message_from_string(raw_email_string)
            #print("Self.Mail: ", self.email_message.keys())

            #log That you received an email
            self.logInfo()

            if self.email_message.get_content_maintype() != 'multipart':
                continue
                #go to next iteration of the loop
            for part in self.email_message.walk():
                #print("This is a part:", part)
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                self.attachmentFilename = part.get_filename()
                print("filename: ", self.attachmentFilename)
                if not self.isJpg():
                    print("Not an jpg")
                    continue
                #et the current dirctory
                dir_path = os.path.dirname(os.path.realpath(__file__))
                #directory of the photos
                directory_path = "%s/%s"%(dir_path, self.PhotoLocation)
                #get the next available name for the new downloaded photo
                fileName = fileNaming.getName(directory_path)
                #calculate the path to save the downloaded image
                dest_path = "%s/%s/%s"%(dir_path,self.PhotoLocation, fileName)
                print(dest_path)

                #download the file
                fp = open(dest_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

    def logInfo(self):
        #log the information of the email received with photos
        try:
            sender = self.email_message['From']
        except:
            sender = "Cant Retrieve Sender"
        try:
            messageID = self.email_message['Message-ID']
        except:
            messageID = "Cant Retrieve messageID"
        try:
            DateSent = self.email_message['Date']
        except:
            DateSent = "Cant Retrieve Date Sent"

        logIntro = "The photo frame has recieved an email, here is the emails info:"
        #create a list of the information
        Info = ["Date Sent:", DateSent, "From:", sender, "Message ID:", messageID]
        #pass this list to a logging function to save the data
        report.logToFile(self.logFilePath, logIntro, Info)

    def logout(self):
        #log of the gMail server
        self.mail.close()
        self.mail.logout()
        print('logged off')

    def isJpg(self):
        if self.attachmentFilename.find('jpg') < 0:
            if self.attachmentFilename.find('jpeg') < 0:
                return False
            else:
                return True
        else:
            return True
