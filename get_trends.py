import os
import pandas as pd
import requests, bs4
import sys
from dateutil.parser import parse


def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False


def get_dates(start_date, end_date):
    dates = pd.date_range(start_date, end_date).tolist()
    all_dates = [str(date).split(' ')[0] for date in dates]
    return all_dates


def get_trends(dates_list, url, out_file):
    trends = {}
    print("Requesting Trends ....")
    for date in dates_list:
        print(date)
        out_file.write("\n" + date + "\n\n")

        req_url = url + date
        resp = requests.get(req_url)
        resp.raise_for_status()

        soup_resp = bs4.BeautifulSoup(resp.text)
        soup_trends = soup_resp.select(".panel .list-group .list-group-item a")

        trends[date] = {}
        for trend in soup_trends:
            tr_id = trend.get('href').split('/')[2]
            tr_name = trend.getText()

            trends[date][tr_id] = tr_name

            out_file.write(tr_id + " " + str(tr_name.encode('utf-8')) + "\n")

    return trends


def print_trends(trends):
    for date in trends:
        print("\n", date, "\n")
        for tr_id in trends[date]:
            print(tr_id, trends[date][tr_id])


def output2file(trends):
    with open("trends.txt", 'wb') as f:
        print("Writing to file ....")
        for date in trends:
            print(date)
            f.write("\n" + date + "\n\n")
            for tr_id in trends[date]:
                f.write(tr_id + " " + str(trends[date][tr_id].encode('utf-8')) + "\n")


def main(arguments):

    if len(arguments)!=3:
        print("Invalid Number of Arguments !!! ")
        return
    elif (not is_date(arguments[1])) or (not is_date(arguments[2])):
        print("One of the dates is Invalid !!!")
        return
    else:
        # Deleting previous trends.txt
        try:
            os.remove('trends.txt')
        except:
            c = 1
        # Intialization
        # start_date = '2017-01-01'  # Date the website started to store information
        # end_date = '2017-12-10'  # Date when the scraping was done
        start_date = arguments[1]
        end_date = arguments[2]
        country_id = '23424922'  # Id for Pakistan
        url = "https://trendogate.com/placebydate/%s/" % country_id

        # Get Dates
        dates_list = get_dates(start_date, end_date)

        out_file = open("trends.txt", "a+")

        # Get Trends
        trends = get_trends(dates_list, url, out_file)

        out_file.close()

main(sys.argv)
