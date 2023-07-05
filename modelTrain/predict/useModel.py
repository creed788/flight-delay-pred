import pandas as pd
import joblib
from sklearn import preprocessing

# load the model
model = joblib.load('modelTrain/predict/delayPredict_0710.pkl')
# load dictionary mapping csv
id = pd.read_csv('modelTrain/predict/dict_id.csv', encoding= 'gbk')
departure = pd.read_csv('modelTrain/predict/dict_departure.csv', encoding= 'gbk')
arrival = pd.read_csv('modelTrain/predict/dict_arrival.csv', encoding= 'gbk')

# Store id, departure, arrival as a dictionary
id_dict = {}
for i in range(len(id)):
    id_dict[id['航班编号'].values[i]] = id['id'].values[i]

departure_dict = {}
for i in range(len(departure)):
    departure_dict[departure['出发机场'].values[i]] = departure['id'].values[i]

arrival_dict = {}
for i in range(len(arrival)):
    arrival_dict[arrival['到达机场'].values[i]] = arrival['id'].values[i]

def predict(data):

    data[0] = departure_dict[data[0]]
    data[1] = arrival_dict[data[1]]

    data = pd.DataFrame(data).T

   # Normalization
    ss_X = preprocessing.StandardScaler()
    data_scaled = ss_X.fit_transform(data)

   # predict
    data_pred = model.predict_proba(data_scaled)
    data_pred = data_pred[0]
    # data_pred 3 digits after the decimal point
    data_pred = [round(i, 3) for i in data_pred]
    return data_pred
# pred = predict(['HET','TYN','Y87566',165,-6.6,-2.1,-11.1,0.0,1038.0,311.0,10.0,2016,12,5,11])

# print('Normal delay probability:',pred[0],'% \Probability of slight delay:',pred[1],'% \n Moderate probability of delay:',pred[2],'% \n Moderate probability of delay:',pred[3],'%')