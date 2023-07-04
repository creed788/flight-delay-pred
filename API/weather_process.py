import os
import pandas as pd

# Read all the files under weather respectively as csv files
def read_weather_csv():
    # # Get all file names under the weather folder
    file_list = os.listdir('API/weather')
    # Loop through all filenames
    for file_name in file_list:
        # read file content
        df = pd.read_csv('API/weather/' + file_name)
        # remove empty lines
        df = df.dropna(axis=0, how='any')

        # remove the same row as the column header
        df = df.drop_duplicates(subset=['Time'], keep='first')

        # delete the last line
        df = df.drop(df.index[-1])

        # Delete all columns with dp['time'].split('/')[2]!=2016
        df = df[df['Time'].str.split('/').str[2] == '2016']
        df['month'] = 0
        df['day'] = 0
        # Create month and day columns
        for i in range(len(df)):
            df['month'].values[i] = df['Time'].values[i].split('/')[1]
            df['day'].values[i] = df['Time'].values[i].split('/')[0]

        # Sort by month and day
        df = df.sort_values(by=['month', 'day'])

        # remove month and day columns

        # write to file
        df.to_csv('API/weather/' + file_name, index=False)

read_weather_csv()