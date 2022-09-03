#CSE303 Project Model 2 : LinearSVC

#%%
#imports
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve , roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

#%%
#reading data files
train_file = pd.read_csv('train.csv')
test_file = pd.read_csv('test.csv')
#%%
print(train_file.info)
print(test_file.info)
#%%
print('Train File null Valuse:\n',train_file.isna().sum()) #No null value found
print('Test File null Valuse:\n',test_file.isna().sum()) #No null value found
train_file = train_file.dropna()
test_file = test_file.dropna()
#%%
print('Train File unique Values:\n',train_file.nunique())
print('Test File unique Values:\n',test_file.nunique())

#%%
train_file = train_file.drop_duplicates()
test_file = test_file.drop_duplicates()
#%%
encoder = LabelEncoder()
scaler = StandardScaler()
#%%
train_file.drop(columns = ['id'] , inplace = True)
test_file.drop(columns = [ 'id'] , inplace = True)

#%%
column = list(test_file.columns)
print(column)
#%%
for i in column:
    encoder.fit(list(train_file[i].values) + list(test_file[i].values))
    train_file[i]= encoder.transform(train_file[i])
    test_file[i] = encoder.transform(test_file[i])

#%%
X = train_file.drop(columns = ['target'])
y = train_file['target']
#%%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=80, shuffle = False)

#%%
X_train[X_train.columns] = scaler.fit_transform(X_train[X_train.columns])
X_test[X_test.columns] = scaler.transform(X_test[X_test.columns])
test_file[test_file.columns] = scaler.transform(test_file[test_file.columns])
#%%
print('Training data:\n', train_file.head())
print('Testing data:\n', test_file.head())
#%%
print('Linear SVC Model\n')
model_lsvc = LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, loss='squared_hinge', max_iter=1000,
          multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
          verbose=0)
model_lsvc.fit(X_train, y_train)
y_pred_lsvc = model_lsvc.predict(X_test)

#%%
#Scores

lsvc_acc_score = accuracy_score(y_test, y_pred_lsvc) * 100
print("Accuracy for LSVC Regression: ", round(lsvc_acc_score, 1), "%" )

p_lsvc = precision_score(y_test, y_pred_lsvc, average='micro') * 100
print('Precision for LSVC Regression: ',round(p_lsvc, 1), "%")

r_lsvc = recall_score(y_test, y_pred_lsvc, average='weighted') * 100
print('Recall for LSVC Regression:  ', round(r_lsvc, 1), "%")

f1_lsvc = f1_score(y_test, y_pred_lsvc) * 100
print('F1-score for LSVC Regression: ', round(f1_lsvc, 1), "%")

rus_lsvc = roc_auc_score(y_test, y_pred_lsvc) * 100
print('ROC AUC Score (LSVC Model):',round(rus_lsvc, 1), "%")

#%%
lsvc_roc_auc = roc_auc_score(y_test, model_lsvc.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, model_lsvc.predict(X_test))
plt.figure()
plt.plot(fpr, tpr, label='LSVC Regression (area = %0.2f)' % lsvc_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([-0.05, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc="lower right")
plt.savefig('lsvc_ROC')
plt.show()

#%%
cm_lsvc = confusion_matrix(y_test, y_pred_lsvc)
print(cm_lsvc)
plot_confusion_matrix(model_lsvc, X_test, y_test) 
plt.title('Confusion Matrix for LSVC Model')
plt.savefig('Log_lsvc') 
plt.show() 
#%%
#New Dataset LSVC
lini =  model_lsvc.predict(test_file)
result1 = pd.read_csv('sample_submission.csv',index_col = 0)
result1['target'] = lini
result1.to_csv('group4_model2_result.csv')
print('Sucessful! Saved New File')