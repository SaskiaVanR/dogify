#from sklearn.preprocessing import LabelEncoder
import keras
from keras.applications import VGG19
from keras.applications import imagenet_utils
#from imutils import paths
import numpy as np

import csv
 
# load the VGG16 network and initialize the label encoder
print("[INFO] loading network...")
#keras.models.load_model("vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5")
model = VGG19(weights=None, include_top=False, input_shape=(32, 32, 3))
print("DONE")
model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5")
imagestrings = []
for i in range(1,50001):
    if i%1000==0:
        print(i)
    imagestrings +=["C:\\Users\\bloom\\OneDrive\\Documents\\GitHub\\dogify\\train\\train\\"+str(i)+".png"] 
    
batchlist = []
i=0
for im in imagestrings:
    if i%1000==0:
        print(i)
    creedimage = keras.preprocessing.image.load_img(im)
    creedarray = keras.preprocessing.image.img_to_array(creedimage)
    creedarray = np.expand_dims(creedarray, axis=0)  
    creedarray = imagenet_utils.preprocess_input(creedarray)
    creedarray = np.vstack(creedarray)
    batchlist +=[creedarray]
    i+=1
print("putting batch together")

batch = np.stack(batchlist)
print("predicting")
features = model.predict(batch)
print("reshaping")
features = features.reshape((features.shape[0], 512))
print("done")
# batch should contain images you want to get features for

# features contains final feature vectors for each image,
# length 262656
targets = []

with open('trainLabels.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rownum = 0
    d = {}
    for row in csv_reader:
        rownum+=1
        if rownum==1:
            continue
        elif rownum==102:
            break
        d[row[0]]=row[1]
        targets +=[row[1]]


    
