#Modified on 4th August 2019

#display Image Tkinter Testing
import tkinter
from PIL import Image, ImageTk
import ImageOrientation as ImagOrient
import time
import os, sys, glob
import sortFiles as SF
from settings import Settings
import random
from datetime import datetime


class DisplayImage():

    def __init__(self, window, path, photosPath, winWidth, winHeight, Interval_secs, recent, new_random_photos, old_random_photos):
        self.window = window
        self.path = path
        self.photosPath = photosPath
        self.windowWidth = winWidth
        self.windowHeight = winHeight
        self.rotation = 0
        self.index = 0
        self.interval = Interval_secs
        self.recent = recent
        self.new_random_photos = new_random_photos
        self.old_random_photos = old_random_photos
        window.config(cursor="none")
        self.photo_list()
        #self.set_up_photo_dir_parameters()
        #display the image
        self.displayImage()


    def check_for_recent_images(self):
        #adds any photos downloaded in the last 48hrs to the front of the
        #order of photos list
        ##48 hours in seconds
        #twoDaysInSecs = 172800
        #first go through the directory and see if any photos were downloaded, in the
        #last 48 hrs
        for file in self.dirlist:
            print(file)
            print(time.time() - os.path.getmtime(file) )
            if (time.time() - os.path.getmtime(file) ) < self.recent:
                #if photos were downloaded in the last 48 hrs then add to the
                #start of the photo list
                print("recent file: ", file)
                self.orderOfPhotos.append(file)

    def photo_list(self):
        #create a list that will have the order to display photos
        self.orderOfPhotos = []
        #get the directory with the photos in`
        self.dir = "%s%s" % (self.path, self.photosPath)
        #sort list into when modified
        self.dirlist = SF.sortFilesDateMod(self.dir)
        #create a current directory list Length, for checking new images
        self.listLength = len(self.dirlist)
        #check for images less than 48 hrs since download in self.dirlist and add to front of photos list in
        self.check_for_recent_images()
        #take the rest of the photos in self.dirlist and produce a random list of photos adding to check_for_new_images
        #produced list
        self.create_photo_list()


    """if more than 30 photos remaining after checking for check_for_recent_images
    randomise next 30 and add to photo list and then add a random selection of
    20 older images. if less than 30 than just add the rest to photolist after they are randomised"""
    def create_photo_list(self):
        num_of_files_left = len(self.dirlist) - len(self.orderOfPhotos)
        if num_of_files_left > 0 and num_of_files_left <= self.new_random_photos:
            temp_list = self.dirlist[len(self.orderOfPhotos):len(self.dirlist)]
            random.shuffle(temp_list)
            self.orderOfPhotos.extend(temp_list)
        elif num_of_files_left > self.new_random_photos:
            temp_list = self.dirlist[len(self.orderOfPhotos):(len(self.orderOfPhotos)+(self.new_random_photos-1))]
            random.shuffle(temp_list)
            self.orderOfPhotos.extend(temp_list)
            older_photos_list = self.dirlist[(len(self.orderOfPhotos)):]
            #print("Older Photots List:", older_photos_list)
            random.shuffle(older_photos_list)
            self.orderOfPhotos.extend(older_photos_list[0:self.old_random_photos])
        print ("Order of Images: ", self.orderOfPhotos)
        self.forDebuggingOrder()

    def forDebuggingOrder(self):
        #add logging for debugging purposes
        filename = "%s%s" % (self.path, "/orderCheck.log")
        print(filename)
        dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.writeTofile(filename, dt)
        self.writeTofile(filename, ": ")
        fileList = []
        i = 0
        for file in self.orderOfPhotos:
            fileList.append(os.path.basename(file))
            text = "File %s: %s"%(i, os.path.basename(file))
            i = i + 1
            self.writeTofile(filename, text)
            self.writeTofile(filename, ", ")
        self.writeTofile(filename, '\n')

        print("order of files: ", fileList)


    def writeTofile(self, filename, str1):
        with open(filename, "a") as logFile:
            logFile.write(str1)


    def check_for_new_images(self):
        #Determine if new files have been added
        #this will be determined everytime the image is changed
        #get a new sorted directory list of photos
        self.newdirList = SF.sortFilesDateMod(self.dir)
        print("Original List Length: ", self.listLength)
        print("New List Length: ", len(self.newdirList))
        #if the new list is different to the old one there are new or removed
        #photos
        if (len(self.newdirList)) != self.listLength:
            #create new directory lists
            self.photo_list()
            #start at photos 0 in the direcotry
            self.index = 0

    def image_rotate(self):
        #determines the orientation of the image
        #and rotates accordingly
        self.rotation = ImagOrient.ImageOrientation(self.imagePath)
        self.image = Image.open(self.imagePath)

        #work out ratios
        if self.rotation == 270 or self.rotation == 90:
            #rotate image
            print("Image is a Portrait")
            self.image = self.image.rotate(self.rotation, expand=True)
        else:
            print("Image is landscape")
            #if rotation 180 then upside, if 0 then fine
            self.image = self.image.rotate(self.rotation, expand=True)

    def resize_image_fit_frame(self):
        #get image dimensions
        self.imageWidth = int(self.image.size[0])
        self.imageHeight = int(self.image.size[1])

        #determine which dimension height or width needs to be reduced the most
        #to fit in the window and select that as the scaling ratio
        if self.windowHeight/self.imageHeight < self.windowWidth/self.imageWidth:
            self.DivideRatio = self.windowHeight/self.imageHeight
        else:
            self.DivideRatio = self.windowWidth/self.imageWidth

        #new image width and height
        self.newWidth = int(self.imageWidth*self.DivideRatio)
        self.newHeight = int(self.imageHeight*self.DivideRatio)

        #resize the image to fit in the window
        self.image = self.image.resize((self.newWidth, self.newHeight), Image.ANTIALIAS)

    def set_up_frame(self):
        #set up the frame in the window
        #create a frame
        self.frame = tkinter.Frame(self.window, height=self.windowHeight, width=self.windowWidth)
        self.frame.grid(row=1, column = 1)
        self.frame.configure(background='black')

    def create_image_label(self):
        #create label with image and position
        self.tkImage = ImageTk.PhotoImage(self.image)
        self.label_image = tkinter.Label(self.frame, image=self.tkImage, borderwidth = 0)
        self.label_image.grid(row=1, column =1)

    def configure_window(self):
        #settings to center the image in the window
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        #remove title from the window
        self.window.wm_attributes('-type','splash')
        self.window.geometry("%sx%s"%(self.windowWidth, self.windowHeight))
        self.window.configure(background='black')

    def displayImage(self):

        self.check_for_new_images()
        #for debugging
        print("Index: ", self.index)
        #get image path
        self.imagePath = self.orderOfPhotos[self.index]
        print(self.imagePath)

        self.image_rotate()

        self.resize_image_fit_frame()

        print("New Height:", self.newHeight)
        print("New Width:", self.newWidth)

        self.set_up_frame()

        self.create_image_label()

        self.configure_window()

        print("Width: ",self.imageWidth)
        print("Height: ",self.imageHeight)
        #self.window.geometry("%sx%s"%(self.imageHeight, self.imageWidth))

        #events of the window and frame
        #self.window.bind("<Button-1>", self.click)
        self.frame.after(self.interval ,self.timer)


    def timer(self):
        print("A timer test")
        #destroy frame and therefore the image
        self.label_image.grid_forget()
        self.label_image.destroy()
        #self.frame.grid_forget()
        #self.frame.destroy()
        #if index at the end of the reset if not move along one
        if self.index < (len(self.orderOfPhotos)-1):
            self.index = self.index + 1
        else:
            self.photo_list()
            self.index = 0
        #display next image
        self.displayImage()

    def click(self, event):
        #called if the window was clicked`
        #determine if the window was clicked on the right or the left
        print(event.x)
        #if clicked on the left hand side. move the images back one
        if (event.x < (self.windowWidth/2)):
            #click with left so go backwards
            if self.index != 0:
                self.index = self.index - 1
            else:
                self.index = self.listLength-1
        else:
            #if click on the right hand side move foreward one
            if self.index < self.listLength-1:
                self.index = self.index + 1
            else:
                self.index = 0

        print("Test")
        print(self.index)
        #display current frame and therefore current image
        self.frame.destroy()
        #display the next image
        self.displayImage()

#################
#MAIN PROGRAME##
################

#get the Settings
#Institate the Settings
frameSettings = Settings()
imagePath = frameSettings.dir_path
photosPath = frameSettings.photo_path
frameWidth = frameSettings.width
frameHeight = frameSettings.height
Intervaltime = frameSettings.time
recentTime = frameSettings.recent
oldRandomPhotos = frameSettings.oldRandomPhotos
newRandomPhotos = frameSettings.newRandomPhotos

root = tkinter.Tk()
#window stays ontop
root.overrideredirect(True)
rt = DisplayImage(root, imagePath, photosPath, frameWidth, frameHeight, Intervaltime, recentTime, newRandomPhotos, oldRandomPhotos)
root.mainloop()
