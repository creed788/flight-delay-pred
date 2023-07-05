from calendar import isleap
import re
from bs4 import BeautifulSoup
from modelTrain.weather_predict.GetData import GetData
import datetime as DT
import csv


def a(t):
    return t.replace(" - ", "0")


# Function: write csv
def write(years, b, c, id):
    """
    :param years: [Year from start date, year from end date]
     :param b: [the number of days from the start date to the current date, the number of days from the end date to the current date]
     :param c: csv file name
    :return: None
    """
    # 1. Create a file object
    f = open(c, 'w', encoding='utf-8', newline='')

    # 2. Build csv write object based on file object
    csv_writer = csv.writer(f)

    # 3. Build the list header
    # , "negAve", "negMax", "negMin"
    csv_writer.writerow(["Time", "Ave_t", "Max_t", "Min_t", "Prec", "SLpress", "Winddir", "Windsp"])
    # Get the current date
    today = DT.datetime.today()
    # leap year fragment
    st = isleap(today.year)
    # Get the date 15 days ago
    week_ago = (today - DT.timedelta(days=b[0])).date()
    # 15 days later
    week_pre = (today + DT.timedelta(days=b[1])).date()
    # From February to March
    if week_ago.month + week_pre.month == 5:
        # If the month of the start date is February, then it is from February to March
        if week_ago.month == 2 and not st == isleap(today.year - years[0]):  # after not means that the following processing will be performed when it is not this year
            if st:  # Because this year spans 2.29 from February to March, other years do not, so we take an extra day "backwards" and subtract one from the start date
                 # Yes this year, not last year or future, so -1
                week_ago -= DT.timedelta(days=1)
            else:
                # Not this year, last year or future, so +1
                 # In the same way, this year is not the same as adding one, because other years have 2.29
                week_ago += DT.timedelta(days=1)

    # crawl data link
     # Site instance
    # http://www.meteomanz.com/sy2?l=1&cou=2250&ind=54511
    # &d1=08
    # &m1=06
    # &y1=2022
    # &d2=21
    # &m2=06
    # &y2=2022
    url = "http://www.meteomanz.com/sy2?l=1&cou=2250&ind=" + id + "&d1=" + str(week_ago.day).zfill(2) + "&m1=" + str(
        week_ago.month).zfill(2) + "&y1=" + str(week_ago.year - years[0]) + "&d2=" + str(week_pre.day).zfill(
        2) + "&m2=" + str(week_pre.month).zfill(2) + "&y2=" + str(week_pre.year - years[1])
    # Display the URL to get the dataset
    print(url)
    g = GetData(url).Get()
    # beautifulsoup parsing web pages
    soup = BeautifulSoup(g, "html5lib")
    # Get <tbody> content
    tb = soup.find(name="tbody")
    # Get tr content
    past_tr = tb.find_all(name="tr")
    for tr in past_tr:
        # Get the content of each td in tr
        text = tr.find_all(name="td")
        flag = False
        negA = negMax = negMin = False
        for i in range(0, len(text)):
            if i == 0:
                text[i] = text[i].a.string
                # The website may have a bug, and it will give the 0th day of each month, such as 00/6/2022, so it must be dropped
                if "00/" in text[i]:
                    flag = True
            elif i == 8:
                # Remove /8, the format displayed on the web page
                text[i] = text[i].string.replace("/8", "")
                print('eighth')
                print(text[8])
            elif i == 5:
                # remove units
                text[i] = text[i].string.replace(" Hpa", "")
                print('fifth')
                print(text[5])
            elif i == 6:
                # Remove the content in parentheses in Fengli
                text[i] = re.sub(u"[º(.*?|N|W|E|S)]", "", text[i].string)
                print('sixth')
                print(text[6])
            else:
                # Get the content of each element
                text[i] = text[i].string
                print('Dividing line：text')
                print(text)
            # Missing data takes null value
            text[i] = "" if text[i] == "-" else text[i]
            text[i] = "" if text[i] == "- " else text[i]
            text[i] = "" if text[i] == "Tr" else text[i]
        print(len(text))
        text = text[0:8]
        # 4. Write the content of the csv file
        if not flag:
            csv_writer.writerow(text)
    # 5. close file
    f.close()
