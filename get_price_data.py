import os
import json
import requests
import sys
import datetime
import math
import pandas as pd


def get_historical_asset_price_data(assets, mertic_id, start_date, end_date):
    # we can sanitize the inputs to this function if we are taking them from the command line and keep filters based on whether
    # the values or start_date and end_date are in correct format or not
    # we can also check if the assets or the metric_id belong to our set of values that are available
    asset_price_dictionary = {}
    date_values = []
    price_list = []
    i = 0

    for asset in assets:
        url = ""
        url = "https://data.messari.io/api/v1/assets/" + asset + "/metrics/" + metric_id + "/time-series?start=" + start_date + "&end=" + \
            end_date + "&interval=1d"  # the value of the interval can be taken as an argument as well for free tier we can support 1 day and 1 week
        response = requests.get(url)
        # also we are assuming that the api will always return the response in the same format(/with same structure)
        data_value = response.json()['data']
        price_list = []
        for data in data_value["values"]:

            if i == 0:
                epoch = math.trunc(int(data[0])/1000)
                date_utc = datetime.datetime.utcfromtimestamp(
                    epoch).strftime('%Y-%m-%d')
                date_values.append(date_utc)

            price_list.append(data[1])

        i = i+1
        asset_price_dictionary[asset.upper()] = price_list

    # print(date_values)
    # print(asset_price_dictionary)

    # reference https://www.javatpoint.com/how-to-create-a-dataframes-in-python
    # NOTE: currently the data frame created is sorted alphabetically and that can be changed if needed
    df = pd.DataFrame(asset_price_dictionary, index=date_values)
    # sorting the data frame by index(/date) inplace
    df.sort_index(inplace=True)
    # here we can append start / end date and the assets in the filename to make it easier to deal with on subsequent calls
    df.to_csv('asset_price_data.csv')
    return df


def get_assets():
    # changing this to api version v2 returns the same result
    url = "https://data.messari.io/api/v1/assets"
    assets_symbol_set = set()
    response = requests.get(url)
    data_value = response.json()['data']
    i = 0
    for data in data_value:
        # we can replace this with slug or name which are unique
        assets_symbol_set.add(data["symbol"])  # symbol is non unique
        # assets_symbol_set.add(data["name"])
        # assets_symbol_set.add(data["slug"])
        i = i+1
    print("total assets returned by this endpoint: " + str(i))
    print(assets_symbol_set)


def get_available_metrics():
    url = "https://data.messari.io/api/v1/assets/metrics"
    metric_id_set = set()
    response = requests.get(url)
    data_value = response.json()['data']
    i = 0
    metric_values = data_value["metrics"]
    for data in metric_values:
        metric_id_set.add(data["metric_id"])
        i = i+1
    print("total metrics returned by this endpoint: " + str(i))
    print(metric_id_set)


if __name__ == "__main__":
    # get_assets()
    # get_available_metrics()
    # if we do not want to pass in the arguments and want to use variables we can set these values
    """
    start_date = "2021-10-10"
    end_date = "2021-10-13"
    assets = ["uni", "luna", "mkr"]
    metric_id = "price"
    dataframe = get_historical_asset_price_data(
    assets, metric_id, start_date, end_date)
    print(dataframe)
    """
    assets = []
    if len(sys.argv) < 5:
        print("please enter appropriate arguments start date, end date, metric and the symbol of the assets \
        you would like to get the data for")
    else:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
        metric_id = sys.argv[3]
        for i in range(4, len(sys.argv)):
            assets.append(sys.argv[i])

        dataframe = get_historical_asset_price_data(
            assets, metric_id, start_date, end_date)
        print(dataframe)
