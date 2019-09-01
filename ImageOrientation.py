#This is a file that
from PIL import Image, ExifTags

def ImageOrientation(ImagePath):

    orientation = 99
    image = Image.open(ImagePath)
    #Produces a dictory of the exif data
    exif = image._getexif()
    #items returns a list of tuples containing key-values pairs
    #loop through the list of key-value pairs
    #print(ExifTags.TAGS)
    try:
        for tag, data in exif.items():
        #ExifTags.TAGS is a dictory of the code-name pairs for
        #exif tags. E.G. 274 is Orientation
        #.get is a dictory method. So get the value of the key tag
        #if its orientation then you can get the data for orientation

        #print(ExifTags.TAGS.get(tag))
        #print(data)

            if ExifTags.TAGS.get(tag) == "Orientation":
                orientation = data
                break

    except:
         #default rotation
         rotation = 0
         #if no exif data then orientation will be a dummy value
         orientation = 99

    #print (orientation)
    #determine the rotation required for the image
    if orientation == 3:
        rotation = 180
    elif orientation == 6:
        rotation = 270
    elif orientation == 8:
        rotation = 90
    else:
        rotation = 0

    print(rotation)
    return rotation


#Path = "/home/spaceman/Programming/python/photoFrame/Photos/20190629_110249.jpg"
#rot = ImageOrientation(Path)
#print(rot)
