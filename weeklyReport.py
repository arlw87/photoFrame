#Weekly report class
import os
import sendEmail as reportEmail

class WeeklyReport():
    def __init__(self, ReportLocation, CounterLocation, DaysBetweenSendingReport):

        self.ReportLocation = ReportLocation
        self.CounterLocation = CounterLocation
        self.DaysBetweenSendingReport = DaysBetweenSendingReport


    def timeToSendReport(self):
        #report should be sent if the frame has been on for 7 days since
        #the last report was sent

        #check if file exists
        if os.path.exists(self.CounterLocation):
            #open counter file
            with open(self.CounterLocation, "r") as counter:
                content = counter.readline()
                print("Report Counter Value: ", content)
            if int(content) < (self.DaysBetweenSendingReport - 1):
                newNum = int(content) + 1
                with open(self.CounterLocation, "w") as counter:
                    counter.write(str(newNum))
                return False
            else:
                with open(self.CounterLocation, "w") as counter:
                    counter.write("0")
                return True
        else:
            with open(self.CounterLocation, "w") as counter:
                counter.write("0")
            return False

    def sendReport(self, txEmail, rxEmail, emailSubject, PSWD, message):
        #in this function an email will be created and sent to the developer
        print("Send Email")
        self.emailSubject = emailSubject
        self.message = message
        self.emailAccountPSWD = PSWD
        self.rxEmail = rxEmail
        self.txEmail = txEmail
        reportEmail.send_email(self.txEmail, self.rxEmail, self.emailAccountPSWD, self.emailSubject, self.ReportLocation, self.message )



#test the class
#CounterLocation = "%s/%s"%(os.path.dirname(os.path.realpath(__file__)),"counter.log")
#wr = WeeklyReport("","","",CounterLocation)
#print(wr.timeToSendReport())
