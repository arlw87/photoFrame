import datetime

def checkTimeImage(justCheckMinutes, minutes):
#get currentDate and time
    currentTime = datetime.datetime.now()
    #print("Passed min list: ", minutes)
    for min in minutes:
        #print("Actual Min: ", currentTime.minute)
        #print("Min to check", min)
        if justCheckMinutes:
            if currentTime.minute == min:
                print("Min Correct")
                return True
    return False


def checkTimeReport(minutes, hours):
    currentTime = datetime.datetime.now()
    if currentTime.minute == minutes and currentTime.hour == hours:
        return True
    else:
        return False

#test the code out
#testTime = datetime.datetime.strptime("21/11/06 22:56", "%d/%m/%y %H:%M")
#print(testTime)
#print(checkTime(False, testTime.minute, testTime.hour))
