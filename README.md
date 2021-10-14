# Historical Asset Price Data from Messari API

Simple module to extract, transform and return historical asset price data using the Messari's API.
[Messari API docs](https://messari.io/api/docs)

## Explanation

The get_historical_asset_price_data will be called if there are enough arguments passed by the user. We are passing the assets list, metric to be fetched, start date and the end date. In the function we are looping through the assets list and fetching the data for those using the api call. We are converting the time value from millisecond to second and converting it to date in the format that we need and storing it into a date_values list to be assigned to the final dataframe as an index. The asset price dictionary has the data for each asset with a list of prices which is being passed to the data frame. The function returns a dataframe with the format:
LUNA MKR UNI
2021-10-10 42.480616 2572.055860 25.128790
2021-10-11 39.280661 2460.887011 24.206328
2021-10-12 39.151339 2448.782439 24.158782
2021-10-13 37.545284 2441.295271 23.447305

These are the endpoints being used:

1. [https://data.messari.io/api/v1/assets/yfi/metrics/price/time-series?start=2021-01-01&end=2021-02-01&interval=1d]
2. [https://data.messari.io/api/v1/assets] //here we can replace version 1 to version 2 and the result remains the same
3. [https://data.messari.io/api/v1/assets/metrics] //here we can replace version 1 to version 2 and the result remains the same

## Usage

Once you have cloned the project

```
git clone https://github.com/dattgoswami/test_solution_5.git
```

navigate to the projects directory and run:

```
python get_price_data.py start_date end_date metric_id asset1 asset2
```

start_date and end_date are of the format yyyy-mm-dd

```
e.g.
python get_price_data.py 2021-10-10 2021-10-13 price uni luna mkr
```

here python can be replaced by python3 if you have that installed on your machine

OR

if you are running it using Spyder(Anaconda) then use this command

```
runfile('get_price_data.py', args='2021-10-10 2021-10-13 price uni luna mkr')
```

If we want to use it without the arguments then we need to uncomment the lines 88 to 96 and comment lines 97 to 110. In this case we will simply run it as:

```
python get_price_data.py
```

## Note

We can choose the opening price or the closing price from the values received for an asset for each day, in here, I have chosen the opening price.
We could also store the average of opening and closing price if needed.

Also, the commented code is left as is to enable debugging. The dataframe is being printed on the console and saved to a csv file under the same directory with name asset_price_data.csv

## Dependencies

Few modules that are needed: requests, pandas.
These can be installed by:

```
pip install module_name
OR
pip3 install module_name
```

Anaconda can be downloaded from here: [https://www.anaconda.com/products/individual]
