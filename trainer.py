import pandas
from sklearn import preprocessing
import numpy
from sklearn import svm
from sklearn import cross_validation as cv
import matplotlib.pylab as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning,
                        module="pandas", lineno=570)

def return_nonstring_col(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]

def svm_classifier_ui(train,query,train_cols):
    pre_list = {}
    clf = svm.SVC(probability=True)
	#print clf.fit(train[train_cols], train['malicious'])
    clf.fit(train[train_cols], train['malicious'])
    e = clf.predict_proba(query[train_cols])
    pre_list['0'] = format(e[0][0] * 100,'0.2f')
    pre_list['1'] = format(e[0][1] * 100,'0.2f')
    pre_list['2'] = format(e[0][2] * 100,'0.2f')
    query['result']=clf.predict(query[train_cols])
    pre_list['result'] = int(query['result'])
    #print pre_list
	#print query[['URL','result']]
        #print query[['result']]
    #return query['result']
    return pre_list

def svm_classifier(train,query,train_cols):
	
	clf = svm.SVC()

	train[train_cols] = preprocessing.scale(train[train_cols])
	query[train_cols] = preprocessing.scale(query[train_cols])
	
	print clf.fit(train[train_cols], train['malicious'])
	scores = cv.cross_val_score(clf, train[train_cols], train['malicious'], cv=30)
	print('Estimated score SVM: %0.5f (+/- %0.5f)' % (scores.mean(), scores.std() / 2))

	query['result']=clf.predict(query[train_cols])
	
	print query[['URL','result']].head(2)

def train(db,test_db):
	
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

	svm_classifier(train_csv,query_csv,train_cols)

	forest_classifier(train_csv,query_csv,train_cols)

def gui_caller(db,test_db):
	
	query_csv = pandas.read_csv(test_db)
	cols_to_keep,train_cols=return_nonstring_col(query_csv.columns)

	train_csv = pandas.read_csv(db)
	cols_to_keep,train_cols=return_nonstring_col(train_csv.columns)
	train=train_csv[cols_to_keep]

    return svm_classifier_ui(train_csv,query_csv,train_cols)
