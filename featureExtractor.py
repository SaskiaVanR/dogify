#from sklearn.preprocessing import LabelEncoder
import keras
from keras.applications import VGG19
#from imutils import paths
import numpy as np
 
# load the VGG16 network and initialize the label encoder
print("[INFO] loading network...")
#keras.models.load_model("vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5")
model = VGG19(weights=None, include_top=False, input_shape=(870, 631, 3))
print("DONE")
model.load_weights("vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5")
creedimage = keras.preprocessing.image.load_img("f.png")
creedarray = keras.preprocessing.image.img_to_array(creedimage)
creedarray = np.expand_dims(creedarray, axis=0)
from keras.applications import imagenet_utils
creedarray = imagenet_utils.preprocess_input(creedarray)
creedarray = np.vstack(creedarray)
batch = np.stack([creedarray]*2)
features = model.predict(batch)
features = features.reshape((features.shape[0], 27 * 19 * 512))

# batch should contain images you want to get features for

# features contains final feature vectors for each image,
# length 262656
