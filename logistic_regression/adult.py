import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import DictVectorizer

data_train=pd.read_csv('adult.data',header=None,names=['age','Workclass','fnlwgt','education',
'education-num','marital-status','occupation','relationship','race','sex',
'capital-gain','capital-loss','hours-per-week','native-country','salary'])
data_test=pd.read_csv('adult.test',header=None,names=['age','Workclass','fnlwgt','education',
'education-num','marital-status','occupation','relationship','race','sex',
'capital-gain','capital-loss','hours-per-week','native-country','salary'])

enc = DictVectorizer()

#data_train.fillna('nan', inplace=True)
data_train.iloc[:, [1,3,5,6,7,8,9,13]]=data_train.iloc[:, [1,3,5,6,7,8,9,13]].replace('[^a-zA-Z0-9?]', '', regex = True)
data_train.iloc[:, [1,3,5,6,7,8,9,13]]=data_train.iloc[:, [1,3,5,6,7,8,9,13]].applymap(str.lower)

#data_test['Workclass'].fillna('nan', inplace=True)
data_test.iloc[:, [1,3,5,6,7,8,9,13]]=data_test.iloc[:, [1,3,5,6,7,8,9,13]].replace('[^a-zA-Z0-9?]', '', regex = True)
data_test.iloc[:, [1,3,5,6,7,8,9,13]]=data_test.iloc[:, [1,3,5,6,7,8,9,13]].applymap(str.lower)
data_test.iloc[:, [14]]=data_test.iloc[:, [14]].replace('[.]', ' ', regex = True)

X, y = data_train.iloc[:, list(range(0,14,1))], np.ravel(data_train.iloc[:, [14]].replace(r' <=50K', '-1').replace(r' >50K','1'))
X_t, y_t = data_test.iloc[:, list(range(0,14,1))], np.ravel(data_test.iloc[:, [14]].replace(r' <=50K ', '-1').replace(r' >50K ','1'))

X_train_categ = enc.fit_transform(X.to_dict('records'))
X_test_categ = enc.transform(X_t.to_dict('records'))

clf_l2_LR = LogisticRegression(C=0.1, penalty='l1', tol=0.00001, max_iter=1000,  intercept_scaling=0.1)
clf_l2_LR.fit(X_train_categ, y)


print('score', clf_l2_LR.score(X_test_categ,y_t))
print ('accuracy', accuracy_score(y_t, clf_l2_LR.predict(X_test_categ)))

#score 0.853940175665
#accuracy 0.853940175665