#!/home/femibyte/local/anaconda/bin/python

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import metrics,svm
from patsy import dmatrix, dmatrices

import re

train_df = pd.read_csv('csv/train.csv', header=0)
test_df = pd.read_csv('csv/test.csv', header=0) 


formula1 = 'C(Pclass) + C(Sex) + Fare'
formula2 = 'C(Pclass) + C(Sex)'
formula3 = 'C(Sex)'
formula4 = 'C(Pclass) + C(Sex) + Age + SibSp + Parch'
formula5 = 'C(Pclass) + C(Sex) + Age + SibSp + Parch + C(Embarked)'
formula6 = 'C(Pclass) + C(Sex) + C(Embarked)'
formula7 = 'C(Pclass) + C(Sex) + Age  + Parch + C(Embarked)'
formula8 = 'C(Pclass) + C(Sex) + SibSp + Parch + C(Embarked)'

formula_map = {'PClass_Sex_Fare' : formula1,
	       'PClass_Sex' : formula2,
	       'Sex' : formula3,
	       'PClass_Sex_Age_Sibsp_Parch' : formula4,
	       'PClass_Sex_Age_Sibsp_Parch_Embarked' : formula5
              }

#formula_map={'PClass_Sex_Embarked' : formula6}

formula_map = {'PClass_Sex_SibSp_Parch_Embarked' : formula8}


kernel_types=['linear','rbf','poly']
kernel_types=['poly']
#kernel_types=['rbf']



def main():
    train_df_filled=fill_null_vals(train_df,'Fare')
    train_df_filled=fill_null_vals(train_df_filled,'Age')
    assert len(train_df_filled)==len(train_df)
    
    test_df_filled=fill_null_vals(test_df,'Fare')
    test_df_filled=fill_null_vals(test_df_filled,'Age')
    assert len(test_df_filled)==len(test_df)

    

    for formula_name, formula in formula_map.iteritems():

        print "name=%s formula=%s" % (formula_name,formula)

        y_train,X_train = dmatrices('Survived ~ ' + formula, 
                                    train_df_filled,return_type='dataframe')
        print "Running SVM with formula : %s" % formula
        print "X_train cols=%s " % X_train.columns
        y_train = np.ravel(y_train)
        for kernel in kernel_types:
            #model = svm.SVC(kernel=kernel,gamma=3)
            model = svm.SVC(kernel=kernel)
            print "About to fit..."
            svm_model = model.fit(X_train, y_train)
            print "Kernel: %s" % kernel
            print "Training score:%s" % svm_model.score(X_train,y_train)
            X_test=dmatrix(formula,test_df_filled)
            predicted=svm_model.predict(X_test)
            print "predicted:%s\n" % predicted[:5]
            assert len(predicted)==len(test_df)
            pred_results=pd.Series(predicted,name='Survived')
            svm_results=pd.concat([test_df['PassengerId'],pred_results],axis=1)
            svm_results.Survived=svm_results.Survived.astype(int)
            results_file='csv/svm_%s_%s.csv' % (kernel,formula_name)
        #results_file = re.sub('[+ ()C]','',results_file)
            svm_results.to_csv(results_file,index=False)
    

def fill_null_vals(df,col_name):
    null_passengers=df[df[col_name].isnull()]
    passenger_id_list=null_passengers['PassengerId'].tolist()
    df_filled=df.copy()
    for pass_id in passenger_id_list:
        idx=df[df['PassengerId']==pass_id].index[0]
        similar_passengers=df[(df['Sex']==null_passengers['Sex'][idx]) & (df['Pclass']==null_passengers['Pclass'][idx])]
        mean_val=np.mean(similar_passengers[col_name].dropna())
        df_filled.loc[idx,col_name]=mean_val
    return df_filled

    
    
if __name__ == '__main__':
    main()

