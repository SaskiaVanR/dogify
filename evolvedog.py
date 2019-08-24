#!/usr/bin/env python3

import random
import time
import sys
import numpy

#---- global variables ----
# mutation variables
sigmaA = 1 # (example) mutation sigma for mutate A
sigmaB = 1 # (example) mutation sigma for mutate B

#stop types
MAX_GEN = 1 #for setting the maximum generations
MIN_CONF = 2 #for setting the minimum dog confidence
MAX_TIME = 3 #for setting max amount of time

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
        self.obj = True


    # mutates the image
    def mutate(self):

        # does different mutations based on randomly generated number p
        p = random.random()
        if p<0.5:
            self.mutateA()
        else:
            self.mutateB()

    # one type of mutation
    def mutateA(self):
        pass

    # another type of mutation
    def mutateB(self):
        pass

    # this function returns a new dogImage object
    # new dogImage must have a /copy/ of the image_data
    def makeCopy(self):
        return self


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
def getRandomRect(image, height=False, width=False):
    # TODO: percentage pixels
    if height==False:
        height=random.randrange(20,100)
    if width==False:
        width=random.randrange(20,100)
    maxHeight = len(origarray)
    maxWidth = len(origarray[0])
    topx = random.randrange(0,maxWidth-width)
    topy = random.randrange(0,maxHeight-height)
    bottomx = topx+width
    bottomy = topy+height
    return([[topy, topx],[bottomy, bottomx]])

# Function that moves the contents of one rectangle into another rectangle of the same size
# Takes arguments for starting Rect and ending Rect, with rectangles defined as they are
# in the comments for getRandomRect
def moveRect(imgarray, startRect, endRect):
    modarray = imgarray
    #TODO: validate input by e.g. verifying size of rects is identical
    height = startRect[1][0] - startRect[0][0]
    endheight = endRect[1][0] - endRect[0][0]
    print("DEBUG: height = " + str(height) + ' ' + str(endheight))
    width = startRect[1][1] - startRect[0][1]
    endwidth = endRect[1][1] - endRect[0][1]
    print("DEBUG: width = " + str(width) + ' ' + str(endwidth))
    for i in range(0, height):
        for j in range(0, width):
            endy = endRect[0][0] + i
            endx = endRect[0][1] + j
            starty = startRect[0][0] + i
            startx = startRect[0][1] + j
            pixel = blur(normDist(endy, endx, endRect[0][1], endRect[0][0], endRect[0][1]+width, endRect[0][0]+height),\
                         modarray[starty][startx], modarray[endy][endx])
            
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
    

print("Hello dog")
if len(sys.argv) != 2:
    #origfile = "f.png" 
    sys.exit("Usage: %s imagefile" % sys.argv[0])

import keras

origfile = sys.argv[1]
orig = keras.preprocessing.image.load_img(origfile)
# Some debug crap
print(type(orig))
print(orig.format)
print(orig.mode)
print(orig.size)
orig.show()
origarray = keras.preprocessing.image.img_to_array(orig)
print(len(origarray))

# for i, row in enumerate(origarray):
#     for j, column in enumerate(origarray):
#         if 50<=i<=100 and 100<=j<=150:
#             origarray[i][j] = [0,0,0]
# newimage = keras.preprocessing.image.array_to_img(origarray)
# newimage.show()

##newarray = origarray
##for i in range(0,10):
##    print(str(i))
##    startRect=getRandomRect(origarray)
##    print(startRect)
##    endRect=getRandomRect(origarray,startRect[1][0] - startRect[0][0],startRect[1][1] - startRect[0][1])
##    print(endRect)
##    newarray = moveRect(newarray, startRect, endRect)
##new = keras.preprocessing.image.array_to_img(newarray)
##new.show()

#fliparray = numpy.flip(origarray, [0])
#flipimage = keras.preprocessing.image.array_to_img(fliparray)
#flipimage.show()




