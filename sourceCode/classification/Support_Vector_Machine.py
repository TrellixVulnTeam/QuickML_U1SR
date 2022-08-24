import numpy as np
import pandas as pd
import matplotlib as mpl
import random
from sklearn import preprocessing

# Using TgAgg backend to make matplotlib thread safe
mpl.use("TkAgg")

# import statsmodels.formula.api 

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
# Importing confusion_matrix function
from sklearn.metrics import confusion_matrix
from matplotlib.colors import ListedColormap
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Support Vector Machine (SVM)
def Support_Vector_Machine(Xtest, Xtrain, Ytest, Ytrain, dataSet):
    '''
    Takes pre processed data and the dataSet which expects the algorithm
    to be placed on its data. Performs Support Vector Machine classification
    on the given dataset and returns a confusion matrix to display the accuracy
    and loss of the ML model. 
    '''
    
    # Formatting the dataSets for analysis
    XTrain = np.array(Xtrain[:,:].transpose()[1:,:].tolist()[0])
    XTest = np.array(Xtest[:,:].transpose()[1:,:].tolist()[0])
    YTrain = np.array(Ytrain[:,:].transpose()[1:,:].tolist()[0])
    YTest = np.array(Ytest[:,:].transpose()[1:,:].tolist()[0])

    # Manually casting to int using labelEncoder class to preserve
    # data integrity. (better than .astype('int'))
    lab_enc = preprocessing.LabelEncoder()

    XTrain = lab_enc.fit_transform(XTrain)
    XTest = lab_enc.fit_transform(XTest)
    YTrain = lab_enc.fit_transform(YTrain)
    YTest = lab_enc.fit_transform(YTest)

    # Create SVM Classifier 
    classifier = SVC(kernel = 'linear', random_state=0)

    # Fit Classifier on to Data 
    classifier.fit(XTrain.reshape(-1,1), YTrain.reshape(-1,1))

    YPred = classifier.predict(XTest.reshape(-1,1))
 
    # Plotting the Confusion Matrix 
    plot_confusion_matrix(classifier, XTest.reshape(-1,1), YTest.reshape(-1,1))

    plt.title(f'Support Vector Classification for {dataSet}')

    plt.legend() 
    
    filename = f'{random.randint(100,999)}'
    plt.savefig(f'../QuickML/webapp/static/{filename}.jpg')

    x = f'../QuickML/webapp/static/{filename}.jpg'

    return x