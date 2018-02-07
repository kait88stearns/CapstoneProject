from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd



def cross_validate(X,y,k=5):
    gbr = GradientBoostingRegressor(learning_rate=0.001, loss='ls', n_estimators=10)
    return cross_val_score(gbr, X, y, cv=k)
    
    
    
def model_GD(df, response='number_of_likes', measure = 'rse'):
    y = df[response]
    X = df.drop([response], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X.as_matrix(), y.as_matrix(), test_size= .15)
    gbr = GradientBoostingRegressor(learning_rate=0.001, loss='ls', n_estimators=10)
    
    gbr.fit(X_train,y_train)
    y_hat = gbr.predict(X_test)
    mse = mean_squared_error(y_test, y_hat)
    rse = np.sqrt(mse)
    if measure == 'rse':
        return rse
    elif  measure == 'mse':
        return mse
    else: 
        raise ValueError('not a valid value for measure') 