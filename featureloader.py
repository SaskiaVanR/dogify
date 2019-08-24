import pickle
import csv
from sklearn.linear_model import LogisticRegression

# opens the file and loads the numpy array into the variable features
with open("CIFAR_features.txt", "rb") as fp:
    features = pickle.load(fp)

targets = []

with open('trainLabels.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rownum = 0
    d = {}
    for row in csv_reader:
        rownum+=1
        if rownum==1:
            continue
        if row[1]=="dog":
            
            d[row[0]]=row[1]
            targets +=[row[1]]
        else:
            d[row[0]]="not dog"
            targets +=["not dog"]

dogcount = 0
notdogcount = 0
smallerfeatures = []
smallertargets = []
for i in range(50000):
    if dogcount==5000 and notdogcount==5000:
        break
    if dogcount!=5000 and targets[i]=="dog":
        dogcount+=1
        smallerfeatures += [features[i]]
        smallertargets += [targets[i]]
    elif notdogcount!=5000 and targets[i]=="not dog":
        notdogcount+=1
        smallerfeatures += [features[i]]
        smallertargets += [targets[i]]
    


clf = LogisticRegression().fit(smallerfeatures, smallertargets)

#clf.predict_log_proba(features)
#clf.predict_proba(features)
