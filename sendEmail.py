#This script contains the function that creates and sends the email alerts
#plain text and attachments
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def send_email(sender_email, receiver_email, password, subject, attachmentLocal, messageText):

    #set message parameters
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    #put a simple message in here
    text = messageText

    #set up the image data
    #read in image data
    fp = open(attachmentLocal, 'rb')
    attachmentData = fp.read()
    fp.close()

    #Create attachment object
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(attachmentData)
    attachment.add_header("Content-Disposition",f"attachment; filename= Report.txt",)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(attachment)

    # Create secure connection with server and send email
    #context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

    print('Email Sent')


##lets test out the Code
#dir_path = os.path.dirname(os.path.realpath(__file__))
#message = "This is an email with a report of the weekly photos sent"
#local = "%s/ImageReport.log"%dir_path
#send_email("nannyphotoframe@gmail.com", "arlw87@googlemail.com", "Angm3r1ng", "Test Report", local, message)
