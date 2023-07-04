from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelTrain.weather_predict.Main_weather_predict import weather_predict_single
from modelTrain.predict.useModel import predict
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import datetime

# Configure the database
hostname = 'localhost'
port = '3306'
database = 'db01'
username = 'root'
pwd = ''
dburl = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, pwd, hostname, port, database)

# Create a database connection object
engine = create_engine(dburl, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# Auxiliary function for the implementation of other functions
def geoDistance(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's mean radius, in kilometers
    return c * r


# Select origin airport
def setDepartureAirport(departureAirport):

    # Delete all data in selectAirport table
    sql = 'delete from selectAirport'
    session.execute(sql)
    session.commit()
    # Insert the starting airport departureAirport into the selectAirport table
    sql = 'insert into selectAirport(departureId) values("{}")'.format(departureAirport)
    session.execute(sql)
    session.commit()
    print('The origin airport has been set to:' + departureAirport)

    # Starting Airport Weather Forecast
    isDeparture = True

    # weather_predict_single(departureAirport, engine, session, isDeparture)

    # Temporarily changed to local fill! ! ! !
    # Get today's date in the form of dd/mm/yyyy
    today = datetime.datetime.now().strftime('%d/%m')
    today = str(today) + '/2016'

    # Read weather/corresponding airport.csv file
    df = pd.read_csv('API/weather/' + departureAirport + '.csv')
    # remove empty lines
    df = df.dropna(axis=0, how='any')

    # Find the number of rows with today in the Time column of df
    index = df[df['Time'] == today].index.tolist()
    # Take out the data of this row and the next 6 rows
    df = df.iloc[index[0]:index[0] + 7, :]

    # Delete all data in the original departureWeather table
    sql = 'delete from departureWeather'
    session.execute(sql)
    session.commit()

    # Insert df into the database
    for i in range(len(df)):
        sql = 'insert into departureWeather(weatherId, avg_temp, max_temp, min_temp, prec, pressure, wind_dir, wind_sp, year, month, day, normal_prob, mild_prob, moderate_prob, serious_prob) values(\'{}\',{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format(
            departureAirport, df['Ave_t'].values[i], df['Max_t'].values[i], df['Min_t'].values[i], df['Prec'].values[i],
            df['SLpress'].values[i], df['Winddir'].values[i], df['Windsp'].values[i], 2023,
            str(df['Time'].values[i]).split('/')[1], str(df['Time'].values[i]).split('/')[0], 0, 0, 0, 0)
        session.execute(sql)
        session.commit()

    sql = 'select * from departureWeather'
    rs = session.execute(sql).fetchall()
    pred = []
    for i in rs:
        pred.append(i)
    session.close()
    return pred

# Select arrival airport
def setArriveAirport(arriveAirport):


    # Get the first row of departureId in the selectAirport table
    sql = 'select departureId from selectAirport limit 1'
    departureAirport = session.execute(sql).fetchone()[0]
    # session.close()

    # Update the arriveId of the row in the selectAirport table departureId = departureAirport to arriveAirport
    sql = 'update selectAirport set arriveId = "{}" where departureId = "{}"'.format(arriveAirport, departureAirport)
    session.execute(sql)
    session.commit()
    print('The arrival airport has been set to:' + arriveAirport)

  
    isDeparture = False
    # weather_predict_single(arriveAirport, engine, session, isDeparture)

    # Temporarily changed to local fill! ! ! ! ! !
     # Get today's date in the form of dd/mm/yyyy
    today = datetime.datetime.now().strftime('%d/%m')
    today = str(today) + '/2016'

    # Read weather/corresponding airport.csv file
    df = pd.read_csv('API/weather/' + arriveAirport + '.csv')
    # remove empty lines
    df = df.dropna(axis=0, how='any')
    print(today)
    # Find the number of rows with today in the Time column of df
    index = df[df['Time'] == today].index.tolist()
    # Take out the data of this row and the next 6 rows
    df = df.iloc[index[0]:index[0] + 7, :]
    print(df['Time'].values[0])
    # Delete all data in the original departureWeather table
    sql = 'delete from arriveWeather'
    session.execute(sql)
    session.commit()

    # Insert df into the database
    print(len(df))
    for i in range(len(df)):
        sql = 'insert into arriveWeather(weatherId, avg_temp, max_temp, min_temp, prec, pressure, wind_dir, wind_sp, year, month, day, normal_prob, mild_prob, moderate_prob, serious_prob) values(\'{}\',{},{},{},{},{},{},{},{},{},{},{},{},{},{})'.format(
            arriveAirport, df['Ave_t'].values[i], df['Max_t'].values[i], df['Min_t'].values[i], df['Prec'].values[i],
            df['SLpress'].values[i], df['Winddir'].values[i], df['Windsp'].values[i], 2023,
            str(df['Time'].values[i]).split('/')[1], str(df['Time'].values[i]).split('/')[0], 0, 0, 0, 0)
        session.execute(sql)
        session.commit()
    
    sql = 'select * from arriveWeather'
    rs = session.execute(sql).fetchall()
    pred = []
    for i in rs:
        pred.append(i)
    session.close()
    return pred

# delay prediction
def delayPredict(hour):
    # Get the first row of departureId in the selectAirport table
    global session
    sql = 'select departureId from selectAirport limit 1'
    departureAirport = session.execute(sql).fetchone()[0]

    # Get the first row of arriveId in the selectAirport table
    sql = 'select arriveId from selectAirport limit 1'
    arriveAirport = session.execute(sql).fetchone()[0]

    # Get the id of a random row in the airline table
     # sql = 'select id from airline order by RAND() limit 1'
     # # Get a random row
    # airlineId = session.execute(sql).fetchone()[0]
    airlineId = 3785
    # Get a row of weatherId of the row where airportId = departureAirport in the airport table
    sql = 'select weatherId from airport where airportId = "{}"'.format(departureAirport)
    weatherId = session.execute(sql).fetchone()[0]

    # Get the longitude and latitude of the rows where airportId = departureAirport and arriveAirport in the airport table
    sql = 'select longitude, latitude from airport where airportId = "{}"'.format(departureAirport)
    departure_longitude = session.execute(sql).fetchone()[0]
    departure_latitude = session.execute(sql).fetchone()[1]
    sql = 'select longitude, latitude from airport where airportId = "{}"'.format(arriveAirport)
    print(arriveAirport)
    arrive_longitude = session.execute(sql).fetchone()[0]
    arrive_latitude = session.execute(sql).fetchone()[1]
    length = geoDistance(departure_longitude, departure_latitude, arrive_longitude, arrive_latitude)

    # Get the weather in the departureWeather table
    sql = 'select * from departureWeather where weatherId = \'{}\''.format(departureAirport)
    rs = session.execute(sql).fetchall()
    weatherList = []
    for i in rs:
        weatherList.append(i)

    for i in range(len(weatherList)):
        # Add departureId, arrivalId, airlineId, length and hour to the list to create a new list
        newList = [departureAirport, arriveAirport, airlineId, length, weatherList[i][1], weatherList[i][2], weatherList[i][3], weatherList[i][4], weatherList[i][5],
                    weatherList[i][6], weatherList[i][7], weatherList[i][8], weatherList[i][9], weatherList[i][10], hour]

        pred = predict(newList)
        # Update the delays in the departureWeather table
        session = Session()
        sql = 'update departureweather set normal_prob = {}, mild_prob = {}, moderate_prob = {}, serious_prob = {} where year = {} and month = {} and day = {}'.format(pred[0], pred[1], pred[2], pred[3], weatherList[i][8], weatherList[i][9], weatherList[i][10])
        session.execute(sql)
        session.commit()
    print('Delay forecast completed')
    # Get normal_prob, mild_prob, moderate_prob, serious_prob in the departureWeather table
    sql = 'select year, month, day, normal_prob, mild_prob, moderate_prob, serious_prob from departureWeather'
    rs = session.execute(sql).fetchall()
    pred = []
    for i in rs:
        pred.append(i)
    session.close()
    return pred

# Get departure weather
def getDepartureWeather():

    #Get the first row of departureId in the selectAirport table
    sql = 'select departureId from selectAirport limit 1'
    departureAirport = session.execute(sql).fetchone()[0]

    # Get a row of weatherId of the row where airportId = departureAirport in the airport table
    sql = 'select weatherId from airport where airportId = "{}"'.format(departureAirport)
    weatherId = session.execute(sql).fetchone()[0]
    print(weatherId)

    # Get the weather in the departureWeather table
    sql = 'select * from departureWeather where weatherId = {}'.format(weatherId)
    rs = session.execute(sql).fetchall()
    weatherList = []
    for i in rs:
        weatherList.append(i)
    session.close()
    # Returns a two-dimensional list of weather and delay information, in the form of:[avg_temp, max_temp, min_temp, prec, pressure, wind_direction, wind_speed, year, month, day]
    return str(weatherList[0:len(weatherList)-1][1:11])

# Get arrival weather:
def getArriveWeather():
    #Get the first row of departureId in the selectAirport table
    sql = 'select departureId from selectAirport limit 1'
    departureAirport = session.execute(sql).fetchone()[0]

    # Get the corresponding arriveId
    sql = 'select arriveId from selectAirport where departureId = "{}"'.format(departureAirport)
    arriveAirport = session.execute(sql).fetchone()[0]

    # Get a row of weatherId of the row where airportId = arriveAirport in the airport table
    sql = 'select weatherId from airport where airportId = "{}"'.format(arriveAirport)
    weatherId = session.execute(sql).fetchone()[0]

    # Get the weather in the arriveWeather table
    sql = 'select * from arriveWeather where weatherId = {}'.format(weatherId)
    rs = session.execute(sql).fetchall()
    weatherList = []
    for i in rs:
        weatherList.append(i)
    session.close()
    #Return a two-dimensional list of weather information in the form of: [avg_temp, max_temp, min_temp, prec, pressure, wind_direction, wind_speed, year, month, day]
    return str(weatherList[0:len(weatherList)-1][1:11])