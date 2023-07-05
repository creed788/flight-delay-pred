from modelTrain.weather_predict.Write import write
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt


# Data preprocessing
def ProcessData(city, id):
    """
    :return:
        [X_train X training data set,
         X_valid Validation set of X training data set,
         y_train Y training data set,
         y_valid Validation set of Y training data set,
         implied_X_test prediction dataset]
     """

     # Use the data of recent years as the training set
     # For example, [1,1], [20, 0] is to use the data from 20 days before today in 2021 to today's data in 2021 as the training set
     # write to csv
    
    id = str(id)
    write([1, 1], [15, 0], "modelTrain/weather_predict/weather_train_train.csv", id)
    write([1, 1], [0, 15], "modelTrain/weather_predict/weather_train_valid.csv", id)
    write([0, 0], [15, 0], "modelTrain/weather_predict/weather_test.csv", id)
    X_test = pd.read_csv("modelTrain/weather_predict/weather_test.csv", index_col="Time", parse_dates=True)
    # Read test and validation sets
    X = pd.read_csv("modelTrain/weather_predict/weather_train_train.csv", index_col="Time", parse_dates=True)
    y = pd.read_csv("modelTrain/weather_predict/weather_train_valid.csv", index_col="Time", parse_dates=True)
    
    # fill in missing values
    my_imputer = SimpleImputer()
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)
    imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
    imputed_X_valid = pd.DataFrame(my_imputer.transform(X_valid))
    imputed_y_train = pd.DataFrame(my_imputer.fit_transform(y_train))
    imputed_y_valid = pd.DataFrame(my_imputer.transform(y_valid))
    imputed_X_test = pd.DataFrame(my_imputer.fit_transform(X_test))

    return [imputed_X_train, imputed_X_valid, imputed_y_train, imputed_y_valid, imputed_X_test]
