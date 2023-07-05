from modelTrain.weather_predict.Main_weather_predict import weather_predict_single
from modelTrain.predict.predict_test import predict
from modelTrain.weather_predict.Main_weather_predict import weather_predict_all
import pandas as pd

# First all forecast weather and then forecast delay
from sql import querySomething, queryAllthing


def predictAll():
    # Predict the data of all airports in the past 7 days
    weather_predict_all()
    # read weather data for all airports
    airport = pd.read_csv("dataset/airport.csv", encoding='gbk')
    weather_dict = {}
    for i in range(len(airport)):
        weather_dict[airport['机场编码'][i]] = pd.read_csv("weather_predict/weatherData/" + airport['机场编码'][i] + ".csv")

   # Predict the weather data in csv and add the results to csv
    for city in weather_dict:
        # add new line
        weather_dict[city]['预测出发延迟'] = float(0)
        weather_dict[city]['预测到达延迟'] = float(0)
        for i in range(len(weather_dict[city])):
            result_departure, result_arive = predict(weather_dict[city].iloc[i][1:8])
            # added to the end of line i
            weather_dict[city].loc[i, '预测出发延迟'] = result_departure
            weather_dict[city].loc[i, '预测到达延迟'] = result_arive
       # write to csv
        weather_dict[city].to_csv("temp_result/" + city + ".csv")


def predictSingle(airportId, engine, session):
    # Forecast the data of a single airport in the past 7 days
    weatherId = weather_predict_single(airportId, engine, session)
    a = querySomething(engine, "weatherinfo", weatherId,"weatherId","*")
    weatherList = []
    for row in a:
        weatherList.append(row)

    weather_dict = {airportId: weatherList}

  # Predict the weather data in csv and add the results to csv
     # add new line
    for i in range(len(weather_dict[airportId])):
        result_departure, result_arrive = predict(weather_dict[airportId][i][2:9])
       # Add to the end of line i

        sql = "update weatherInfo set delayDeparture = " + str(
            result_departure[0]) + ",delayArrive = "+str(result_arrive[0]) +" where date = "+'\''+str(weather_dict[airportId][i][1])+'\''
        session.execute(sql)
        session.commit()
        session.close()

    # write to csv
    #weather_dict[airportId].to_csv("/temp_result/" + airportId + ".csv")

    # Pass the csv into the database
    print(weather_dict[airportId])


# predictFromWeatherAll()

'''
airport = pd.read_csv("dataset/airport.csv", encoding= 'gbk')
weather_dict = {}
for i in range(len(airport)):
    weather_dict[airport['机场编码'][i]] = pd.read_csv("weather_predict/weatherData/" + airport['机场编码'][i] + ".csv")
for city in weather_dict:
    print(weather_dict[city].iloc[0])
'''
