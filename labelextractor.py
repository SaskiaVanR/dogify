targets = []
import csv
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


# d contains a dictionary with the key being the index for the image
# and the value being either dog or not dog
# target is the same, except it is a list

# there are 50 thousand labels
# 5000 are dog, 45000 are not dog

# code for logistic regression
#from sklearn.linear_model import LogisticRegression
#clf = LogisticRegression().fit(features, targets)
#clf.predict(features)
#clf.predict_log_proba(features)
#clf.predict_proba(features)

