#from sklearn.preprocessing import LabelEncoder
import keras
from keras.applications import VGG19
from keras.applications import imagenet_utils
from PIL import Image
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
##batchlist = []
##i=0
##for im in imagestrings:
##    if i%1000==0:
##        print(i)
##    creedimage = keras.preprocessing.image.load_img(im)
##    creedarray = keras.preprocessing.image.img_to_array(creedimage)
##    creedarray = np.expand_dims(creedarray, axis=0)  
##    creedarray = imagenet_utils.preprocess_input(creedarray)
##    creedarray = np.vstack(creedarray)
##    batchlist +=[creedarray]
##    i+=1
##print("putting batch together")
##
##batch = np.stack(batchlist)
##print("predicting")
##features = model.predict(batch)
##print("reshaping")
##features = features.reshape((features.shape[0], 512))
##print("done")
# batch should contain images you want to get features for

# features contains final feature vectors for each image,
# length 262656
##targets = []
##
##with open('trainLabels.csv', mode='r') as csv_file:
##    csv_reader = csv.reader(csv_file, delimiter=',')
##    rownum = 0
##    d = {}
##    for row in csv_reader:
##        rownum+=1
##        if rownum==1:
##            continue
##        elif rownum==102:
##            break
##        d[row[0]]=row[1]
##        targets +=[row[1]]


    
ace = keras.preprocessing.image.load_img("ace.jpg")
smallace = ace.resize((224,224), Image.BILINEAR)
acearray = keras.preprocessing.image.img_to_array(smallace)
bestp, best = predictImage(acearray)
