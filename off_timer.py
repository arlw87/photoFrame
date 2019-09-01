#Script to turn off raspberry pi at a predefined time
import datetime
import time
import os


# def writeToLog(filename, text):
#     with open(fileName, "a+") as logFile:
#         logFile.write(text)
#         logFile.write('\n')
#
# currentTime = datetime.datetime.now()
# turnOffHour = 14
# turnOffMin = 13
# turnOffcmd = "sudo poweroff"
#
# fileName = "/home/pi/Programming/python/nannyPhotoFrame/offTimer.log"

cmd = "sudo shutdown -h 23:15"

temp = os.popen(cmd).readline()

print("script run")

time.sleep(600)

# writeToLog(fileName, temp)
#
# while True:
#     writeToLog(fileName, ("Current Hour: %s"% currentTime.hour))
#     writeToLog(fileName, ("Hour to turn off: %s" %turnOffHour))
#     writeToLog(fileName, ("Current min: %s" %currentTime.minute))
#     writeToLog(fileName, ("min to turn off: %s"% turnOffMin))
#     #if the current hour is the hour to turn off then
#     #turn off
#     #and currentTime.minute == turnOffMin:
#     if currentTime.hour == turnOffHour:
#         print("Hour right")
#         if currentTime.minute == turnOffMin:
#             print("Minute Right")
#             print("Turn Off")
#             writeToLog(fileName, "About to turn off")
#             temp = os.popen(turnOffcmd).readline()
#             writeToLog(fileName, temp)
#     time.sleep(20)
#     #sleep for 10 minutes
