import pickle

# opens the file and loads the numpy array into the variable features
with open("CIFAR_features.txt", "rb") as fp:
    features = pickle.load(fp)
