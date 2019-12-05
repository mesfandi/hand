
"""
@author: Mtajic
"""


import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, tree, datasets
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.externals.six import StringIO
from sklearn.model_selection import cross_validate

from skimage import io
from skimage.filters import gaussian
from skimage.transform import resize
from IPython.display import Image

from sklearn.ensemble import RandomForestClassifier

class DataSet:
    def __init__(self, inputs=None, targets=None):
        self.inputs = [] if inputs is None else inputs
        self.targets = [] if targets is None else targets


if __name__ == '__main__':
    dataset = DataSet()
    print('Loading Training Data...')
    labels = ['01_palm', '02_l', '03_fist', '04_fist_moved', '05_thumb',
              '06_index', '07_ok', '08_palm_moved', '09_c', '10_down', ]

    # TODO: need to shuffle data before partitioning
    # 75% to train
    for i in range(10):
        for label in labels:
            for j in range(1, 151):  # 201):
                label.split()
                image = io.imread('data/leapGestRecog/0' +
                                  str(i) + '/' +
                                  label + '/frame_0' +
                                  str(i) + '_' +
                                  label[0:2] + '_' +
                                  str(j).zfill(4) + '.png')
                # TODO: should we flatten or resize here?
                img_blurred = gaussian(image, sigma=1.65)
                dataset.inputs.append(resize(img_blurred, (60, 160), preserve_range=True).flatten())
                dataset.targets.append(label)

    # shuffle data
    x_train, y_train = shuffle(dataset.inputs, dataset.targets)

    # Model Selection

    print('Model Selection...')
    
    testScores = {}
    myMaxScore = 0
    bestFunctionPrameters = ""
    clf_cv5 = ""
    for i in [6, 7, 8, 9, 10]:
        for j in ["gini", "entropy"]:
            clf_rft = RandomForestClassifier(criterion=j, n_estimators=100, max_features=240, max_depth=i, random_state=0) #15

            # perform 5-fold cross validation for each model
            scores = cross_validate(clf_rft, x_train, y_train, scoring='precision_macro', cv=5, return_estimator=True)
            testScores[j + "_" + str(i)] = scores["test_score"]
            myScore = np.max(scores["test_score"], axis=0)
            print(j + "_" + str(i), " Score: ", str(myScore))
            if myScore > myMaxScore:
                clf_rft_cv5 = scores["estimator"][np.argmax(scores["test_score"], axis=0)]
                myMaxScore = myScore
                bestFunctionPrameters = j + "_" + str(i)


 	# Training

    print('Training...')
    bst_rft = clf_rft_cv5

    labels = ['01_palm', '02_l', '03_fist', '04_fist_moved', '05_thumb',
              '06_index', '07_ok', '08_palm_moved', '09_c', '10_down', ]
    print('Loading Testing Data...')
    # 25% to test

    test_data = DataSet()
    for i in range(10):
        for label in labels:
            for j in range(151, 201):  # 1, 201):
                label.split()
                image = io.imread('data/leapGestRecog/0' +
                                  str(i) + '/' +
                                  label + '/frame_0' +
                                  str(i) + '_' +
                                  label[0:2] + '_' +
                                  str(j).zfill(4) + '.png')
                img_blurred = gaussian(image, sigma=1.65)
                test_data.inputs.append(resize(img_blurred, (60, 160), preserve_range=True).flatten())
                test_data.targets.append(label)

    print('Testing...')
    predicted = bst_rft.predict(test_data.inputs)
    print("\nClassification Report")

    print(classification_report(test_data.targets, predicted))
    print("\nConfusion Matrix")
    print(confusion_matrix(test_data.targets, predicted))




	#clf_rft = clf_rft.fit(X_train, y_train)
	#y_pred_rft=clf_rft.predict(X_test)
y_train_score_rft=bst_rft.predict(x_train)
#print("accuracy of the model is:\nTest ", accuracy_score(test_data.targets, predicted, normalize=True, sample_weight=None))
#print('Train',accuracy_score(y_train, y_train_score_rft, normalize=True, sample_weight=None))

		
	# creating the box plot for model-selection
s = testScores.values()
labels = testScores.keys()
fig = plt.figure(figsize=(8, 6))

plt.boxplot([x for x in s], 0, '', 1)
plt.xticks([y + 1 for y in range(len([x for x in s]))], labels, rotation=70)
plt.xlabel('Models(metric and max depth)')
plt.ylabel('Accuracy')
t = plt.title('Box plot of HyperParameters with 5-fold cross validation')
plt.show()
