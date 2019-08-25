#!/usr/bin/env python3

import random
import time
import sys
import numpy
from PIL import Image
import keras
from keras.applications import VGG19
from keras.applications import imagenet_utils
#from imutils import paths
import numpy as np

import csv

def predictImage(imagearray):
    a = np.copy(imagearray)
    a = np.expand_dims(a, axis=0)
    a = imagenet_utils.preprocess_input(a)
    a = np.vstack(a)
    b = [a,a]
    batch = np.stack(b)
    f = model.predict(batch)
    bestp = f[0][0]
    best = 0
    for i in range(151,269):
        if f[0][i]>=bestp:
            best = i
            bestp = f[0][i]
    return bestp, best



    
# load the VGG16 network and initialize the label encoder
print("[INFO] loading network...")
#keras.models.load_model("vgg19_weights_tf_dim_ordering_tf_kernels.h5")
model = VGG19(weights=None, input_shape= (224,224, 3))

model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels.h5")
print("DONE")
ace = keras.preprocessing.image.load_img("ace.jpg")
smallace = ace.resize((224,224), Image.BILINEAR)
acearray = keras.preprocessing.image.img_to_array(smallace)
bestp, best = predictImage(acearray)

#---- global variables ----
# mutation variables
sigmaA = 1 # (example) mutation sigma for mutate A
sigmaB = 1 # (example) mutation sigma for mutate B

#stop types
MAX_GEN = 1 #for setting the maximum generations
MIN_CONF = 2 #for setting the minimum dog confidence
MAX_TIME = 3 #for setting max amount of time

REC_PERC_MIN = 0.025
REC_PERC_MAX = 0.2


#---- end of global variables ----

# class for storing the image to evolve
class dogImage(object):

    # image data needed on initialisation
    def __init__(self, image_data):
        self.image_data = image_data
        # objective calculated later, False when not yet calculated
        self.obj = False

    # calculates objective value and stores it under self.obj
    def calcObj(self):
        self.obj, a_ = predictImage(self.image_data)
        return
        self.obj = self.calcSimilarity(targetDog)
        return
        total = 0
        for row in self.image_data[::20]:
            for column in row[::20]:
                for rgb in column:    
                    total += rgb
        self.obj = total


    def calcSimilarity(self, targetDog):
        score = 0
        h = len(self.image_data)
        w = len(self.image_data[0])
        for row in range(20):
            row = int(h*row/20)
            for column in range(20):
                column = int(w*column/20)
                #print(row, column, targetDog[row][column])
                if 0<=targetDog[row][column][0]<=5 and\
                    250<=targetDog[row][column][1]<=255 and\
                    0<=targetDog[row][column][2]<=5:
                    continue
                score += - colourDist(targetDog[row][column], \
                                      self.image_data[row][column])
##                for rgb in range(3):
##                    #print((255 -abs(self.image_data[row][column][rgb]-\
##                                 #targetDog[row][column][rgb])))
##                    score += (255 -abs(self.image_data[row][column][rgb]-\
##                                 targetDog[row][column][rgb]))
##                    #print(score)
        return score


    # mutates the image
    def mutate(self):

        # does different mutations based on randomly generated number p
        p = random.random()
        for i in range(0,random.randrange(5)):
            self.mutateRect()


    # one type of mutation
    def mutateA(self):
        pass

    # another type of mutation
    def mutateB(self):
        endRect=getRandomRectEnd(self.image_data,random.randrange(5,20),random.randrange(5,20))
        hue = numpy.array([(0.7 +random.random()*0.6),\
                           (0.7 +random.random()*0.6),(0.7 +random.random()*0.6)])
        endheight = endRect[1][0] - endRect[0][0]
        endwidth = endRect[1][1] - endRect[0][1]
        for i in range(0, endheight):
            for j in range(0, endwidth):
                endy = endRect[0][0] + i
                endx = endRect[0][1] + j
                self.image_data[endRect[0][0] + i][endRect[0][1] + j] *=hue
        

    def mutateRect(self):
        startRect=getRandomRectStart(self.image_data)
        endRect=getRandomRectEnd(self.image_data,startRect[1][0] - startRect[0][0],startRect[1][1] - startRect[0][1])
        self.image_data = moveRect(self.image_data, original,startRect, endRect)

    # this function returns a new dogImage object
    # new dogImage must have a /copy/ of the image_data
    def makeCopy(self):
        return dogImage(numpy.copy(self.image_data))

    def display(self):
        img = keras.preprocessing.image.array_to_img(self.image_data)
        img.show()


def endCondition(stopType, stopValue, gen, bestConf, currentTime):
    if stopType==MAX_GEN:
        return gen>stopValue
    elif stopType==MIN_CONF:
        return bestConf>=stopValue
    elif stopType==MAX_TIME:
        return currentTime>=stopValue
    else:
        #pretend it is max time of 10 seconds
        return currentTime>=10


# ---- evolves startImage to be more dog ----
#
# Inputs:
# startImage = image to be turned into dog
# numChildren = number of children generated per generation
# stopType = type of stop condition. MAX_GEN, MIN_CONF, or MAX_TIME
#            if not properly specified, defaults to MAX_TIME
# stopValue = the value (of stopType) to stop evolving at
#            if stopType not properly specified, defaults to 10 seconds
#
# Output:
# parentHistory = list of parents for each generation
#                 parentHistory[-1] is the final image
# totalGen = total number of generations
# runTime = total run time


def Evolve(startImage, numChildren, stopType, stopValue):
    # initialise parent
    parent = startImage
    parent.calcObj()

    # initialise tracker variables
    bestConf = parent.obj
    gen = 1
    startTime = time.time()
    currentTime = time.time() - startTime

    # initialise parent history
    parentHistory = [parent]

    # runs until endCondition(...) is True
    while not endCondition(stopType, stopValue, gen, bestConf, currentTime):

        # make, mutate, and evaluate children      
        children = [parent.makeCopy() for i in range(numChildren)]
        [child.mutate() for child in children]
        [child.calcObj() for child in children]

        # find the best child, if better than parent
        best = parent
        for child in children:
            if child.obj>bestConf:
                best = child
                bestConf = child.obj

        # best is now the parent, add it to history
        parent = best
        parentHistory += [parent]

        # update stats
        currentTime = time.time() - startTime
        gen += 1

        # some stats for nerds
        print("Generation:",gen,"\tBest conf:", bestConf, "\tRun time (s):",\
              round(currentTime,1))

    # get final times
    totalGen = gen - 1
    runTime = startTime - time.time()
    return(parentHistory, totalGen, runTime)


# function that returns the position of a random rectangle in an image,
# optionally taking the size of the rectangle as an argument
# returns two arrays of two, in the form [row, column],[row,column]
# for the top left and bottom right corners of the rectangle
def getRandomRectStart(image, height=False, width=False):
    # TODO: percentage pixels
    maxHeight = len(image)
    maxWidth = len(image[0])
    if height==False:
        height=random.randrange(int(maxHeight*REC_PERC_MIN),
                                int(maxHeight*REC_PERC_MAX))
    if width==False:
        width=random.randrange(int(maxWidth*REC_PERC_MIN),
                                int(maxWidth*REC_PERC_MAX))
    
    topx = random.randrange(0,maxWidth-width)
    topy = random.randrange(0,maxHeight-height)
    bottomx = topx+width
    bottomy = topy+height
    return([[topy, topx],[bottomy, bottomx]])

def getRandomRectEnd(image, height, width):
    maxHeight = len(image)
    maxWidth = len(image[0])
    topx = random.randrange(0,maxWidth-width)
    topy = random.randrange(0,maxHeight-height)
    bottomx = topx+width
    bottomy = topy+height
    #if targetDog[topy][topx][0]==0 and targetDog[topy][topx][1]==255 and\
       #targetDog[topy][topx][2]==0:
        #return getRandomRectEnd(image, height, width)
    return([[topy, topx],[bottomy, bottomx]])

# Function that moves the contents of one rectangle into another rectangle of the same size
# Takes arguments for starting Rect and ending Rect, with rectangles defined as they are
# in the comments for getRandomRect
def moveRect(imgarray, original, startRect, endRect):
    modarray = imgarray
    maxHeight = len(modarray)
    maxWidth = len(modarray[0])
    hue = numpy.array([(0.9 +random.random()*0.2),(0.9 +random.random()*0.2),(0.9 +random.random()*0.2)])
    #TODO: validate input by e.g. verifying size of rects is identical
    height = startRect[1][0] - startRect[0][0]
    endheight = endRect[1][0] - endRect[0][0]
    #print("DEBUG: height = " + str(height) + ' ' + str(endheight))
    width = startRect[1][1] - startRect[0][1]
    endwidth = endRect[1][1] - endRect[0][1]
    #print(height, width, maxHeight, maxWidth)
    #print("DEBUG: width = " + str(width) + ' ' + str(endwidth))
    for i in range(0, height):
        for j in range(0, width):
            endy = endRect[0][0] + i
            endx = endRect[0][1] + j
            if not 0<=endx<maxWidth or not 0<=endy<maxHeight:
                continue
            starty = startRect[0][0] + i
            startx = startRect[0][1] + j
            pixel = blur(normDist(endy, endx, endRect[0][1], endRect[0][0], \
                                  endRect[0][1]+width, endRect[0][0]+height),\
                         modarray[starty][startx], modarray[endy][endx])
            #pixel = original[startRect[0][0] + i][startRect[0][1] + j]
            modarray[endRect[0][0] + i][endRect[0][1] + j] = pixel
    return modarray


def distToEdge(value, firstEdge, secondEdge):
    return min(abs(firstEdge-value), abs(secondEdge-value))

def normDist(pixely, pixelx, topx, topy, bottomx, bottomy):
    minDist = min(distToEdge(pixely, topy, bottomy),distToEdge(pixelx, topx, bottomx))
    return minDist


def blur(minDist, rgbstart, rgbend):
    if minDist>15:
        blurAmount = 0
    else:
        blurAmount = 1 - minDist/15
    return((blurAmount*rgbend + (1-blurAmount)*rgbstart))
    

def colourDist(c1, c2):
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)**(1/2)

print("Hello dog")
if len(sys.argv) != 2:
    #origfile = "f.png" 
    sys.exit("Usage: %s imagefile" % sys.argv[0])

import keras
import tensorflow as tf
targetimage = keras.preprocessing.image.load_img("ace_green.jpg")
targetDog = keras.preprocessing.image.img_to_array(targetimage)
targetHeight = len(targetDog)
targetWidth = len(targetDog[0])

origfile = sys.argv[1]

im1 = Image.open(origfile)
im2 = im1.resize((224,224), Image.BILINEAR)
im2.save("fresize.jpg")
orig = keras.preprocessing.image.load_img("fresize.jpg")
# Some debug crap
##print(type(orig))
##print(orig.format)
##print(orig.mode)
##print(orig.size)
orig.show()
origarray = keras.preprocessing.image.img_to_array(orig)

##print(len(origarray))

# for i, row in enumerate(origarray):
#     for j, column in enumerate(origarray):
#         if 50<=i<=100 and 100<=j<=150:
#             origarray[i][j] = [0,0,0]
# newimage = keras.preprocessing.image.array_to_img(origarray)
# newimage.show()

##newarray = origarray
##for i in range(0,10):
##    print(str(i))
##    startRect=getRandomRectStart(origarray)
##    print(startRect)
##    endRect=getRandomRectEnd(origarray,startRect[1][0] - startRect[0][0],startRect[1][1] - startRect[0][1])
##    print(endRect)
##    newarray = moveRect(newarray, startRect, endRect)
##new = keras.preprocessing.image.array_to_img(newarray)
##new.show()

#fliparray = numpy.flip(origarray, [0])
#flipimage = keras.preprocessing.image.array_to_img(fliparray)
#flipimage.show()
original = origarray
creed = dogImage(origarray)
creedChild = creed.makeCopy()
#creedChild.image_data = creedChild.image_data*0
parentHistory, totalGen, runTime = Evolve(creedChild, 5, MAX_GEN, 300)
best = parentHistory[-1]
best.display()
