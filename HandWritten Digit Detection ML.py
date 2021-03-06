# -*- coding: utf-8 -*-
"""-YudhisthirSharma.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fo0S3KtF00d_6auBtt7myhwDAn6H5jzZ

**Required Modules**
"""

import sklearn
import pandas as pd
import numpy as np
from IPython.display import Image

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier

from sklearn import tree

from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV

"""**Importing Dataset**"""

df = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/semeion/semeion.data", delimiter = r"\s+",
                header=None )

print(df.head())

df.shape

"""**Extracting actual output column**"""

X = pd.DataFrame(df)

X = X.drop([256,257,258,259,260,261,262,263,264,265], axis=1)

type(X)

X.shape

label_df = pd.DataFrame(df.iloc[:,[256,257,258,259,260,261,262,263,264,265]])

label_df.shape

label_df.head()

label_df.rename(columns={256:0, 257:1, 258:2, 259:3, 260:4, 261:5, 262:6, 263:7, 264:8, 265:9 }, inplace=True)

label_df.head()

label_df['y'] = label_df.apply(lambda x: label_df.columns[x.argmax()], axis = 1)

label_df.head()

label_df.tail()

y = label_df['y']
type(y)

""" **Train Test and Split**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=5)

X_train.shape

y_train.shape

X_test.shape

y_test.shape

""" K Nearest Neighbors (KNN)"""

clf_knn = KNeighborsClassifier()

k_range = range (1,6)

knn_weight_options = ['uniform','distance']

knn_algorithm_options = ['ball_tree', 'kd_tree', 'brute']

knn_params = {'n_neighbors':k_range, 'weights':knn_weight_options, 'algorithm': knn_algorithm_options}

knn_grid = GridSearchCV(clf_knn, knn_params, cv=10, scoring='accuracy')

knn_grid.fit(X,y)

knn_grid.best_params_

knn_grid.best_score_

knn_grid.best_estimator_



"""Decision Tree"""

clf_dt= tree.DecisionTreeClassifier(random_state=10)

dt_splitter = ['best','random']

dt_criterion = ['gini', 'entropy']

dt_params = {'splitter':dt_splitter , 'criterion':dt_criterion}

dt_grid = GridSearchCV(clf_dt, dt_params, cv=10, scoring='accuracy')

dt_grid.fit(X,y)

dt_grid.best_params_

dt_grid.best_score_

dt_grid.best_estimator_



"""Final Model"""

clf_final = KNeighborsClassifier(algorithm='brute', leaf_size=30, metric='minkowski',
           metric_params=None, n_jobs=1, n_neighbors=4, p=2,
           weights='distance')

clf_final.fit(X_train,y_train)

y_pred = clf_final.predict(X_test)

print (metrics.accuracy_score(y_test,y_pred))



"""Confusion Matrix"""

cm = confusion_matrix(y_test, y_pred)

cm

labels = [0,1,2,3,4,5,6,7,8,9]
df_cm = pd.DataFrame(cm, index = [i for i in labels],
                  columns = [i for i in labels])
plt.figure(figsize = (10,10))

sns.heatmap(df_cm, annot=True)
plt.xlabel('Predicted', fontsize=20)
plt.ylabel('Actual', fontsize=20)



"""Precision and Recall"""

scr_clf_knn = precision_recall_fscore_support(y_test,y_pred, average='weighted')

print ("classifier's precision: "+str(scr_clf_knn[0]) )
print ("classifier's recall: "+str(scr_clf_knn[1]) )
print ("classifier's fbeta_score: "+str(scr_clf_knn[2]) )

X_test.head()

y_test[:5]

type(y_test)

y_test_df = y_test.to_frame()

y_test_df.head()

y_test_df['y_pred'] = pd.Series(y_pred, index=y_test_df.index)

y_test_df.index[y_test_df.y != y_test_df.y_pred]

wrong_list = [1519, 149, 1153, 1158, 1562, 568]
y_test_df.loc[wrong_list]

def make_image (index_num):
    one_row = X.loc[index_num] # get the record from the X dataset
    one_values = one_row.values # convert the series to a numpy array
        
    i = 16 # values in one array
    j = 0
    img = np.array(one_values[:16])
    while i <= len(one_values):
        temp_array = np.array(one_values[j:i])
        img = np.vstack((img,temp_array))
        j = i   
        i += 16

    # Plot image
    plt.imshow(img,cmap=plt.cm.gray_r,interpolation="nearest")
    plt.show()
    
    print ("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    
    print (y_test_df.loc[index_num]) # will work only for index numbers in the testing datasets
    return

"""Wrongly predicted numbers"""

make_image(1519)

make_image(149)

make_image(1153)

make_image(1158)

make_image(1562)

make_image(568)



"""Correctly Pridicted Numbers"""

make_image(599)

make_image(977)

make_image(362)

