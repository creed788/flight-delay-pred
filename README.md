# flight-delay-pred
# Note ⚠⚠⚠

## database

The database initialization file is in the branch of `dataset-and-model`, all.sql under the design folder,

**Notice! ! , because the crawler website made an error during the weather forecast during the defense, so I temporarily switched to another method, and I needed to add `year, month, day, normal_prob, mild_prob, moderate_prob, serious_prob` of `departureweather` to the table `arriveweather` the same attributes of the , and remove the `date` attribute **

Secondly, the data of the INSERT `airline` and `airport` tables are required, respectively in `modelTrain/predict/dict_id.csv` of `delay-master` branch and `dataset/airport` of `dataset-and-model` branch .csv`

Finally don't forget to start reconfiguring your (cloud) database in `API/algorithm.py` and `API/loginAndRegister.py`

## Weather data forecast

Because during the defense, the crawled weather website was temporarily maintained, so I was forced to replace the weather forecast with directly reading the news on the same day in previous years, and now it can be reused. If you need to add weather forecast, you can re-algorithm.py (if I If I remember correctly) Restore the weather forecast function

<!-- ALL-CONTRIBUTORS-LIST: START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
# project
Prediction system for flight delay information based on flight and weather information in previous years

Data Cleansing Project

1. First, manually make an airport-city code reference dictionary according to the original flight information data corresponding to the weather information website, in which only some airports are selected

2. The latitude and longitude corresponding to the filled airport

3. First perform the first cleaning: delete the departure and arrival airports that are not in the given reference airport dictionary

4. Carry out the second cleaning: delete the duplicate items of the route at the same time (that is, the flight with the same departure point and arrival point)

5. Among them, the processing of the most original data set includes:

   Calculate the planned departure, arrival and actual departure and arrival time through the original timestamp

   Calculate the distance between each airport through the latitude and longitude between different airports and integrate it into the corresponding information column of each flight

6. Crawling and filling weather information through the constructed airport-city reference dictionary

   First construct the weather information file .CSV of each day in different cities

   Carry out the corresponding web crawler to read the data and write to the city weather file

   Through the city->locate the file to be accessed; estimated departure date->locate to the specific item to be filled

7. Then save and write, and get the initially cleaned data set
