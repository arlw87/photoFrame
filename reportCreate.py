# this file call a function to log files downloaded to be
# sent to developer regularly

def logToFile(fileName, Intro, Info):
    str1 = Intro + " "
    for text in Info:
        str1 += text
        str1 += " "

    with open(fileName, "a") as logFile:
        logFile.write(str1)
        logFile.write('\n')

#for testing
#Intro = "Have received an email! Here is some inforamtion from it: "
#list = ["sender", "Date", "Sup"]
#logToFile("test.txt", Intro, list)
