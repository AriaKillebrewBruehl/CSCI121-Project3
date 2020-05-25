# File: ImageShop.py

"""
This program is the starter file for the ImageShop application, which
implements the "Load" and "Flip Vertical" buttons.
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton
from GrayscaleImage import createGrayscaleImage, luminance

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def ImageShop():
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth()) / 2
        y = (gw.getHeight() - image.getHeight()) / 2
        gw.add(image, x, y)

    def loadButtonAction():
        """Callback function for the Load button"""
        filename = chooseInputFile()
        if filename != "":
            setImage(GImage(filename))

    def flipVerticalAction():
        """Callback function for the FlipVertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))
            
    def flipHorizontalAction():
        """Callback function for the FlipHorizontal button"""
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))
            
    def rotateRightAction():
        """Callback function for the RotateRight button"""
        if currentImage is not None:
            setImage(rotateRight(currentImage))
            
    def rotateLeftAction():
        """Callback function for the RotateLeft button"""
        if currentImage is not None:
            setImage(rotateLeft(currentImage))
            
    def grayscaleAction():
        """Callback function for the grayscale button"""
        if currentImage is not None:
            setImage(createGrayscaleImage(currentImage))
            
    def greenScreenAction():
        """Callback function for the GreenScreen button"""
        if currentImage is not None:
            setImage(greenScreen(currentImage))
    def equalizeAction():
        """Callback function for the Equalize button"""
        if currentImage is not None:
            setImage(equalize(currentImage))
        
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    #Add buttons
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton("Flip Horizontal", flipHorizontalAction)
    addButton("Rotate Right", rotateRightAction)
    addButton("Rotate Left", rotateLeftAction)
    addButton("Grayscale", grayscaleAction)
    addButton("Green Screen", greenScreenAction)
    addButton("Equalize", equalizeAction)

# Creates a new GImage from the original one by flipping it vertically.

def flipVertical(image):
    array = image.getPixelArray()
    return GImage(array[::-1])

def flipHorizontal(image):
    array = image.getPixelArray()
    height = len(array)
    for i in range(height):   
        array[i] = array[i][::-1]
    return GImage(array)

def rotateRight(image):
    array = image.getPixelArray()
    height = len(array)
    width = len(array[0])
    newarray = [[0 for x in range(height)] for x in range(width)]
    for i in range(height): 
        for j in range(width):
            newarray[j][height - 1 - i] = array[i][j]
    return GImage(newarray)
    
def rotateLeft(image):
    array = image.getPixelArray()
    height = len(array)
    width = len(array[0])
    newarray = [[0 for x in range(height)] for x in range(width)]
    for i in range(height): 
        for j in range(width):
            newarray[width - 1 - j][i] = array[i][j]
    return GImage(newarray)

def greenScreen(image):
    array = image.getPixelArray()
    height = len(array)
    width = len(array[0])
    
    filename = chooseInputFile()
    if filename != "":
        newImage = GImage(filename)   
        newarray = newImage.getPixelArray()
    
    for i in range(height): 
        for j in range(width):
            if isntGreen(newarray[i][j]):
                array[i][j] =  newarray[i][j]
            
    return GImage(array)         
        
def isntGreen(pixel):
    r = GImage.getRed(pixel)
    g = GImage.getGreen(pixel)
    b = GImage.getBlue(pixel)
    
    if r >= b:
        maxRB = r 
    else:
        maxRB = b
        
    if g > 2*maxRB:
        return False
    else:
        return True 
    
def equalize(image):
    array = image.getPixelArray()
    height = len(array)
    width = len(array[0])
    colors = [0] * 256 
    cumulative = [0] * 256 
    total = 0
    
    for i in range(height): 
        for j in range(width):
            x = luminance(array[i][j])
            colors[x] += 1 
    for i in range(len(colors)):
        total += colors[i]
        cumulative[i] = total
           
    for i in range(height): 
        for j in range(width):
            x = luminance(array[i][j])
            newLum = (255 * cumulative[x]) //  (height * width) 
            array[i][j] = GImage.createRGBPixel(newLum, newLum, newLum) 
    return GImage(array)
      
   
# Startup code

if __name__ == "__main__":
    ImageShop()
