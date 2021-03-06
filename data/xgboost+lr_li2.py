import xgboost as xgb
import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import roc_auc_score
from xgboost import plot_tree
import matplotlib.pyplot as plt
import json
import re

train_path="../data/agaricus.txt.train"
test_path="../data/agaricus.txt.test"

xgtrain=xgb.DMatrix(train_path)
xgtest=xgb.DMatrix(test_path)

X_train,y_trian=load_svmlight_file(train_path)
X_test,y_test=load_svmlight_file(test_path)
watchlist=[(xgtrain,'train'),(xgtest,'test')]

model_sklearn=xgb.XGBClassifier(nthread=4, learning_rate=0.08,
                            n_estimators=10, max_depth=5, gamma=0, subsample=0.9, colsample_bytree=0.5)
model_sklearn.fit(X_train,y_trian)
params=model_sklearn.get_xgb_params()

model_xgboost=xgb.train(params,xgtrain,num_boost_round=10,evals=watchlist)

y_pred_train_sklearn=model_sklearn.predict_proba(X_train)[:,1]
y_pred_test_sklearn=model_sklearn.predict_proba(X_test)[:,1]
sklearn_train_auc=roc_auc_score(y_trian,y_pred_train_sklearn)
sklearn_test_auc=roc_auc_score(y_test,y_pred_test_sklearn)

print ('sklearn_train_auc:%.4f'% sklearn_train_auc)
print ('sklearn_test_auc:%.4f'% sklearn_test_auc)


y_pred_train_xgboost=model_xgboost.predict(xgtrain)
y_pred_test_xgboost=model_xgboost.predict(xgtest)
#xgboost_train_auc=roc_auc_score(y_train,y_pred_train_xgboost)
#xgboost_test_auc=roc_auc_score(y_test,y_pred_test_xgboost)

#print ("xgboost_train_auc:%.4f"% xgboost_train_auc)
#print ("xgboost_test_auc:%.4f"% xgboost_test_auc)

X_train_leaves=model_sklearn.apply(X_train)
X_test_leaves=model_sklearn.apply(X_test)

xgtrain_leaves=model_xgboost.predict(xgtrain,pred_leaf=True)
xgtest_leaves=model_xgboost.predict(xgtest,pred_leaf=True)

def write_leaves(leavesFile,X_train_leaves):
    (rows,cols)=X_train_leaves.shape
    cum_count = np.zeros((1, cols), dtype=np.int32)
    outfile = open(leavesFile, 'w')
    for j in range(cols):
        if j == 0:
            cum_count[0][j] = len(np.unique(X_train_leaves[:, j]))
        else:
            cum_count[0][j] = len(np.unique(X_train_leaves[:, j])) + cum_count[0][j - 1]
    for j in range(cols):
        if j==0:
            dat=dict(zip(np.unique(X_train_leaves[:,j]),range(1,cum_count[0][0]+1)))
        else :
            dat=dict(zip(np.unique(X_train_leaves[:,j]),range(cum_count[0][j-1]+1,cum_count[0][j]+1)))
        #json.dump(dat,outfile,ensure_ascii=False)
        #outfile.write('\n')
        data=str(dat)
        outfile.write('{0}\t{1}\t\n'.format(j, data[1:len(data)-1]))
    outfile.close()
write_leaves('../data/leaves.txt',X_train_leaves)


def write_leaves_json(leavesFile,X_train_leaves):
    (rows,cols)=X_train_leaves.shape
    cum_count = np.zeros((1, cols), dtype=np.int32)
    outfile = open(leavesFile, 'w')
    for j in range(cols):
        if j == 0:
            cum_count[0][j] = len(np.unique(X_train_leaves[:, j]))
        else:
            cum_count[0][j] = len(np.unique(X_train_leaves[:, j])) + cum_count[0][j - 1]
    for j in range(cols):
        if j==0:
            dat=dict(zip(np.unique(X_train_leaves[:,j]),range(1,cum_count[0][0]+1)))
        else :
            dat=dict(zip(np.unique(X_train_leaves[:,j]),range(cum_count[0][j-1]+1,cum_count[0][j]+1)))
        #json.dump(dat,outfile,ensure_ascii=False)
        #outfile.write('\n')
        json.dump(dat,outfile)
        #a=json.dumps(dat)
        #outfile.write(a)
        outfile.write('\n')
    outfile.close()
write_leaves('../data/leaves',X_train_leaves)


def get_transform_leaves(xgtrain_leaves,leaves,mapfile):
    # 如果leaves是json文件的话'
    (rows,cols)=xgtrain_leaves.shape
    for j in range(cols):
        keymapDict={}
        for i in range(rows):
            leaves[i,j]=mapfile[j][xgtrain_leaves[i,j]]














#plot_tree(model_sklearn,num_trees=0)
#plt.show()
#plot_tree(model_xgboost,num_trees=0)
#plt.show()