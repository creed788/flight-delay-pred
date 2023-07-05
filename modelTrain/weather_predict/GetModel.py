from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.metrics import mean_absolute_error
from modelTrain.weather_predict.ProcessData import ProcessData


# train and save the model
def GetModel(city, id, a="modelTrain/weather_predict/Model.pkl"):
    """
    :param a: model file name
    :return:
        [socre: MAE evaluation results,
        X_test: prediction dataset]
    """
    # get the data
    [X_train, X_valid, y_train, y_valid, X_test] = ProcessData(city, id)
 # random tree forest model
    model = RandomForestRegressor(random_state=0, n_estimators=1001)
    # train the model
    model.fit(X_train, y_train)
    # Forecasting model, using last week's data
    preds = model.predict(X_valid)
    # Evaluate with MAE
    score = mean_absolute_error(y_valid, preds)
    # save the model locally
    joblib.dump(model, a)
    # return MAE
    return [score, X_test]


